#!/usr/bin/env python3
"""Notify Microsoft Teams only after Cline completion gates pass."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def validate_gates(args: argparse.Namespace) -> list[str]:
    failures = []
    if args.notification_choice != "enabled":
        failures.append("notification-choice must be enabled")
    if args.quality_result != "PASS":
        failures.append("quality-result must be PASS")
    if not args.evidence or not all(path.is_file() for path in args.evidence):
        failures.append("all evidence files must exist")
    if args.mode == "plan":
        if args.plan_review not in {"Ready", "Ready with Assumptions"}:
            failures.append("plan-review must be Ready or Ready with Assumptions")
    elif args.mode == "implementation":
        for name in ("build_result", "test_result", "review_result"):
            if getattr(args, name) != "PASS":
                failures.append(f"{name.replace('_', '-')} must be PASS")
        if args.verifier_result != "APPROVE":
            failures.append("verifier-result must be APPROVE")
    elif args.verifier_result != "APPROVE":
        failures.append("verifier-result must be APPROVE")
    return failures


def event_id(args: argparse.Namespace) -> str:
    evidence = "\n".join(f"{path.resolve()}:{path.stat().st_mtime_ns}" for path in args.evidence)
    material = f"{args.mode}\n{args.title}\n{args.summary}\n{evidence}"
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:20]


def build_payload(args: argparse.Namespace, notification_id: str) -> dict:
    mode_label = {"plan": "計画", "implementation": "実装", "workflow": "Workflow"}[args.mode]
    lines = [
        f"Cline {mode_label}完了: {args.title}",
        args.summary,
        f"Quality Gate: {args.quality_result}",
    ]
    if args.mode == "plan":
        lines.append(f"Plan Review: {args.plan_review}")
    elif args.mode == "implementation":
        lines.extend([
            f"Build: {args.build_result}",
            f"Test: {args.test_result}",
            f"Review: {args.review_result}",
            f"Verifier: {args.verifier_result}",
        ])
    else:
        lines.append(f"Verifier: {args.verifier_result}")
    lines.append(f"Notification ID: {notification_id}")
    return {"text": "\n".join(lines)}


def send(webhook_url: str, payload: dict, retries: int = 3) -> int:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        webhook_url,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                status = response.getcode()
                if 200 <= status < 300:
                    return status
                raise RuntimeError(f"Teams webhook returned HTTP {status}")
        except (urllib.error.URLError, TimeoutError, RuntimeError):
            if attempt + 1 == retries:
                raise
            time.sleep(2**attempt)
    raise RuntimeError("Teams webhook retry loop ended unexpectedly")


def write_receipt(path: Path, args: argparse.Namespace, notification_id: str, status: str, http_status: int | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    receipt = {
        "notification_id": notification_id,
        "mode": args.mode,
        "title": args.title,
        "status": status,
        "http_status": http_status,
        "quality_result": args.quality_result,
        "evidence": [str(item) for item in args.evidence],
        "sent_at": datetime.now(timezone.utc).isoformat() if status == "SENT" else None,
    }
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def already_sent(path: Path, notification_id: str) -> bool:
    if not path.is_file():
        return False
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return receipt.get("status") == "SENT" and receipt.get("notification_id") == notification_id


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", required=True, choices=("plan", "implementation", "workflow"))
    parser.add_argument("--notification-choice", required=True, choices=("enabled", "disabled"))
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--quality-result", required=True, choices=("PASS", "PASS WITH MINOR FIXES", "NEEDS REVISION", "FAIL", "NOT RUN"))
    parser.add_argument("--plan-review", choices=("Ready", "Ready with Assumptions", "Needs Revision", "Blocked"))
    parser.add_argument("--build-result", choices=("PASS", "FAIL", "NOT RUN"))
    parser.add_argument("--test-result", choices=("PASS", "FAIL", "NOT RUN"))
    parser.add_argument("--review-result", choices=("PASS", "FAIL", "NOT RUN"))
    parser.add_argument("--verifier-result", choices=("APPROVE", "REJECT", "ESCALATE_HUMAN", "NOT RUN"))
    parser.add_argument("--evidence", required=True, action="append", type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    failures = validate_gates(args)
    if failures:
        print(json.dumps({"status": "NOT_SENT", "gate_failures": failures}, ensure_ascii=False), file=sys.stderr)
        return 2
    notification_id = event_id(args)
    payload = build_payload(args, notification_id)
    if args.dry_run:
        print(json.dumps({"status": "DRY_RUN", "notification_id": notification_id, "payload": payload}, ensure_ascii=False, indent=2))
        return 0
    if already_sent(args.receipt, notification_id):
        print(json.dumps({"status": "ALREADY_SENT", "notification_id": notification_id}, ensure_ascii=False))
        return 0
    webhook_url = os.environ.get("TEAMS_WORKFLOW_WEBHOOK_URL")
    if not webhook_url:
        print("TEAMS_WORKFLOW_WEBHOOK_URL is not set", file=sys.stderr)
        return 3
    try:
        http_status = send(webhook_url, payload)
    except (urllib.error.URLError, TimeoutError, RuntimeError) as exc:
        print(f"Teams notification failed: {type(exc).__name__}", file=sys.stderr)
        return 4
    write_receipt(args.receipt, args, notification_id, "SENT", http_status)
    print(json.dumps({"status": "SENT", "notification_id": notification_id, "http_status": http_status}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
