# Stacked Pull Requests

GitHub shipped native stacked PR support in public preview on **July 31, 2026**, via the `gh stack` CLI extension. This doc covers the core workflow.

## What a "stack" is

A stack is an ordered chain of PRs in the same repo, where each PR's base branch is the previous PR's branch instead of `main`. This lets you split a large change into focused, independently reviewable layers that still land together.

```
main ← PR1 (auth-layer) ← PR2 (auth-ui) ← PR3 (auth-tests)
```

## Setup

```
gh extension install github/gh-stack
```

Requires `gh` CLI 2.0+.

## Core workflow

| Step | Command | What it does |
|---|---|---|
| 1 | `gh stack init my-first-layer` | Creates the bottom branch of the stack, based on `main` |
| 2 | edit code, `git add .`, `git commit -m "..."` | Normal git work on that branch |
| 3 | `gh stack add next-layer` | Creates the next branch on top of the current one (or `gh stack add -Am "message"` to stage+commit+branch in one shot) |
| 4 | repeat 2–3 for each layer | Build up as many branches/layers as needed |
| 5 | `gh stack submit` | Pushes every branch and creates all PRs on GitHub, auto-wired with correct base branches |
| 6 | `gh stack view` | Shows the whole stack: branches, PR links, status |

## Keeping the stack in sync

- `gh stack sync` — fetch, rebase, push, and update PR state in one command. Use this most often after addressing review feedback.
- `gh stack rebase` — cascading rebase across the stack (e.g. after `main` moves). Flags: `--downstack`, `--upstack`, `--no-trunk`, `--continue`, `--abort`.
- `gh stack modify` — interactive TUI to reorder, split, fold, or drop layers mid-stack. Operations: drop (x), fold down (d), fold up (u), insert below/above (i/I), move (Shift+arrows), rename (r), undo (z).

## Navigating a stack

- `gh stack up [n]` / `gh stack down [n]` — move n branches away from/toward trunk
- `gh stack top` / `gh stack bottom` / `gh stack trunk` — jump to stack extremes
- `gh stack switch` — interactively pick a branch to check out
- `gh stack checkout` — check out a stack by number, PR number, URL, or branch name (works for other people's stacks too)

## Landing a stack

- `gh stack merge` — merges the whole stack (or a prefix of it) atomically, respecting merge queues and required checks. Flags: `--merge-method`, `--merge`, `--squash`, `--rebase`, `-y/--yes`.

## Other commands

- `gh stack link` — link existing PRs into a stack on GitHub without local tracking
- `gh stack push` — push active branches to remote (uses per-branch `--force-with-lease`)
- `gh stack unstack` (alias `delete`) — remove a stack from local tracking / unstack on GitHub (`--local` for local-only)
- `gh stack alias` — create a short alias (default `gs`) for faster typing
- `gh stack feedback` — open a feedback discussion in the gh-stack repo

## Non-CLI alternative (GitHub website)

1. Create your initial PR targeting `main`.
2. Create subsequent PRs, setting each base branch to the previous PR's branch, then select **Create stack**.
3. Repeat for additional layers.

If you already have open PRs with linearly dependent branches, GitHub shows a recommendation banner to link them as a stack automatically.

## Exit codes (gh stack CLI)

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Generic error |
| 2 | Not in a stack / stack not found |
| 3 | Rebase conflict |
| 4 | GitHub API failure |
| 5 | Invalid arguments or flags |
| 6 | Branch belongs to multiple stacks |
| 7 | Rebase already in progress |
| 8 | Stack locked by another process |
| 9 | Stacked PRs not enabled for repository |
| 10 | Modify session interrupted; recovery needed |

## Sources

- [About stacked pull requests](https://docs.github.com/en/pull-requests/get-started/about-stacked-prs)
- [Quickstart for stacked pull requests](https://docs.github.com/en/pull-requests/get-started/stacked-prs-quickstart)
- [Creating stacked pull requests](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-stacked-pull-requests)
- [Stacked pull requests CLI commands](https://docs.github.com/en/pull-requests/reference/stacked-prs-cli-commands)
- [Roll out stacked pull requests to your organization](https://docs.github.com/en/pull-requests/tutorials/roll-out-stacked-prs)
