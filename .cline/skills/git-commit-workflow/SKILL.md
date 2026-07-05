---
name: git-commit-workflow
description: Create a local feature branch, commit intended changes there, and push that feature branch to the matching remote branch. Use when the user asks to prepare Git commits, create a featureBranch such as feature#na#1, stage intended files, commit, push to remote featureBranch, or publish completed work without touching main directly.
---

# Git Commit Workflow

Create a local feature branch, commit intended changes there, and push it to the matching remote branch.

## Purpose

Keep Git operations controlled and reviewable by avoiding direct work on `main`. Use a local `featureBranch` as the normal place for commits, then push it to the same branch name on the remote.

Never stage, commit, push, reset, delete, or overwrite changes blindly.

## Use This Skill When

- The user asks to commit work
- The user asks to push to GitHub or another remote
- The user asks to prepare a Git commit
- The user asks to create or use a feature branch
- The user asks to check what will be committed
- The user asks to resolve a simple push rejection
- The user asks to add a remote or change a remote URL

## Do Not Use This Skill For

- Code review only
- Implementation work before changes exist
- Destructive cleanup such as reset, clean, checkout, or file deletion unless explicitly requested
- GitHub issue or PR review workflows that need a dedicated GitHub review skill

Use `review-loop` for review-only requests. Use `implementation-loop` when code needs to be changed before committing.

## Branch Model

Default behavior:

```txt
local featureBranch -> remote featureBranch
```

Do not commit directly on `main` or push directly to `origin/main` unless the user explicitly requests it.

Recommended branch names:

```txt
feature#<name>#<number>
fix#<name>#<number>
docs#<name>#<number>
chore#<name>#<number>
```

Examples:

```txt
feature#na#1
fix#login#2
docs#cline-rules#1
chore#memory-bank#1
```

If the user writes `/feature#na#1`, treat the leading `/` as a chat-style prefix and use `feature#na#1` as the actual Git branch name.

## Feature Branch Process

1. Run `git status -sb`.
2. Confirm the current branch:
   - `git branch --show-current`
3. Confirm the remote:
   - `git remote -v`
4. If already on the intended feature branch, stay there.
5. If on `main`, create and switch to a feature branch:
   - `git switch -c feature#<name>#<number>`
6. If on an unrelated branch, ask before switching branches.
7. If the target feature branch already exists locally:
   - `git switch <featureBranch>`
8. If the target feature branch exists only on the remote:
   - `git fetch origin <featureBranch>`
   - `git switch -c <featureBranch> --track origin/<featureBranch>`

## Commit Process

1. Run `git status -sb`.
2. Inspect the diff before staging:
   - `git diff`
   - `git diff --staged` when files are already staged
3. Confirm the current branch is the intended feature branch.
4. Identify the intended scope from the user request.
5. If unrelated changes exist, ask which files belong in the commit.
6. Stage only intended files with explicit paths.
7. Re-check `git status -sb`.
8. Create a concise commit message.
9. Commit on the local feature branch.
10. Report the commit hash and summary.

## Push Process

1. Confirm the current branch is the feature branch:
   - `git branch --show-current`
2. Confirm the remote target:
   - `git remote -v`
3. Push the local feature branch to the matching remote feature branch:
   - `git push -u origin <featureBranch>`
4. If push is rejected because the remote has new work:
   - Run `git fetch origin <featureBranch>`.
   - Inspect remote commits and changed files before merging.
   - Prefer a normal merge or rebase only when it is safe and clear.
   - Do not force push unless the user explicitly requests it and understands it rewrites remote history.
5. If SSH auth fails but GitHub CLI HTTPS auth is available, switch to the equivalent HTTPS remote only after confirming the target repository is the same.

## Safety Rules

- Never use `git add -A` when unrelated files may exist.
- Prefer explicit file paths for staging.
- Do not commit or push directly on `main` unless explicitly requested.
- Do not push local `main` to remote `main` as the default workflow.
- Ensure local feature branch and remote feature branch use the same branch name unless the user requests otherwise.
- Never commit secrets, tokens, credentials, private keys, or local environment files.
- Never run `git reset --hard`, `git clean`, or force push without explicit user approval.
- Never overwrite user changes.
- Do not hide failed checks or failed pushes.
- If authentication blocks push, report the exact blocker and required user action.

## Commit Message Rules

- Use a short imperative or descriptive message.
- Prefer messages like:
  - `add cline workflow rules`
  - `add git feature branch workflow skill`
  - `update memory bank progress`
- Avoid vague messages like:
  - `fix`
  - `update`
  - `changes`

## Final Response Format

```md
## Git Result

- Branch:
- Local featureBranch:
- Remote featureBranch:
- Commit:
- Remote:
- Push:
- Notes:
```

If only a local commit was created, say that push was not requested or did not complete.
