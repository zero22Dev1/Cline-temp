import importlib.util
import tempfile
import unittest
import json
from argparse import Namespace
from pathlib import Path
from unittest.mock import MagicMock, patch


SCRIPT = Path(__file__).parents[1] / "scripts" / "notify_teams.py"
SPEC = importlib.util.spec_from_file_location("notify_teams", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def arguments(root, mode="plan"):
    evidence = root / "evidence.md"
    evidence.write_text("verified", encoding="utf-8")
    return Namespace(
        mode=mode, title="Task", summary="Done", quality_result="PASS",
        notification_choice="enabled",
        plan_review="Ready" if mode == "plan" else None,
        build_result="PASS" if mode == "implementation" else None,
        test_result="PASS" if mode == "implementation" else None,
        review_result="PASS" if mode == "implementation" else None,
        verifier_result="APPROVE" if mode in {"implementation", "workflow"} else None,
        evidence=[evidence], receipt=root / "receipt.json", dry_run=False,
    )


class TeamsCompletionNotifierTest(unittest.TestCase):
    def test_plan_requires_ready_review(self):
        with tempfile.TemporaryDirectory() as temp:
            args = arguments(Path(temp))
            args.plan_review = "Needs Revision"
            self.assertIn("plan-review", " ".join(MODULE.validate_gates(args)))

    def test_disabled_choice_rejects_notification(self):
        with tempfile.TemporaryDirectory() as temp:
            args = arguments(Path(temp))
            args.notification_choice = "disabled"
            self.assertIn("notification-choice", " ".join(MODULE.validate_gates(args)))

    def test_implementation_requires_test_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            args = arguments(Path(temp), "implementation")
            args.test_result = "NOT RUN"
            self.assertIn("test-result", " ".join(MODULE.validate_gates(args)))

    def test_workflow_requires_verifier_approval_without_code_gates(self):
        with tempfile.TemporaryDirectory() as temp:
            args = arguments(Path(temp), "workflow")
            self.assertEqual([], MODULE.validate_gates(args))
            args.verifier_result = "REJECT"
            self.assertIn("verifier-result", " ".join(MODULE.validate_gates(args)))

    def test_payload_does_not_contain_webhook(self):
        with tempfile.TemporaryDirectory() as temp:
            args = arguments(Path(temp), "implementation")
            payload = MODULE.build_payload(args, MODULE.event_id(args))
            self.assertNotIn("webhook", str(payload).lower())
            self.assertIn("Test: PASS", payload["text"])

    def test_sent_receipt_prevents_duplicate(self):
        with tempfile.TemporaryDirectory() as temp:
            args = arguments(Path(temp))
            notification_id = MODULE.event_id(args)
            args.receipt.write_text(json.dumps({
                "status": "SENT", "notification_id": notification_id
            }), encoding="utf-8")
            self.assertTrue(MODULE.already_sent(args.receipt, notification_id))

    @patch("urllib.request.urlopen")
    def test_send_accepts_2xx(self, urlopen):
        response = MagicMock()
        response.getcode.return_value = 202
        response.__enter__.return_value = response
        urlopen.return_value = response
        self.assertEqual(202, MODULE.send("https://example.invalid/hook", {"text": "done"}))


if __name__ == "__main__":
    unittest.main()
