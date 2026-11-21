# Git workflow

Longer reference for the rules in [CLAUDE.md](../CLAUDE.md).

## Repository layout

| Path | What it is |
| --- | --- |
| `/workspace/development` | `frappe_docker` repo (Dev Container). Not this project. |
| `/workspace/development/frappe-bench` | The bench. Site: `development.localhost` (developer mode on). |
| `/workspace/development/frappe-bench/apps/frappe_shop` | **This repo**: `jaguar-mahdi/frappe-shop` on GitHub (public). |

Installed apps on the site: `frappe`, `erpnext`, `payments`, `webshop`, all on `version-16`.

## Protection on `main` (GitHub Ruleset)

- Changes reach `main` only through a pull request (PR).
- Claude Code may open and merge PRs (`gh pr merge --squash`) only after all required checks pass;
  never `--admin`, never a bypass. `strict` is on: a branch must be up to date with `main` before merge.
- Squash merge only: all commits of a PR become one commit on `main`, titled with the PR title.
- Linear history: no merge commits on `main`.
- Required status checks: `Server` (`.github/workflows/ci.yml`),
  `Frappe Linter` and `Vulnerable Dependency Check` (`.github/workflows/linter.yml`).

## Everyday flow

```bash
cd /workspace/development/frappe-bench/apps/frappe_shop
pwd
git switch main
git pull --ff-only origin main          # update main without creating a merge commit
git switch -c <type>/<short-kebab-description>
# ... edit files ...
git add <files>
pre-commit run --all-files              # same check CI runs
git commit -m "<type>: <summary>"
git push -u origin <branch>
gh pr create --base main --title "<type>: <summary>" --body-file <file>   # "## What / ## Why"
gh pr checks <number> --watch           # wait for Server, Frappe Linter, Vulnerable Dependency Check
gh pr merge <number> --squash --delete-branch   # only when every required check passed
```

`pre-commit run --all-files` checks files that git tracks (committed or staged),
so new files must be `git add`-ed first or they are skipped.

## Conventional Commits

Format: `<type>(<optional scope>): <summary in imperative mood>`

| Type | Use for |
| --- | --- |
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code meaning change |
| `refactor` | Code change that is neither a fix nor a feature |
| `test` | Adding or fixing tests |
| `ci` | CI configuration (`.github/workflows`, Dependabot) |
| `chore` | Maintenance, tooling, repo housekeeping |
| `build` | Build system or dependencies |

## Learning log format

Every task ends with a new entry at the bottom of [learning-log.md](learning-log.md), written in Arabic
with English terms in inline code:

1. Date (`YYYY-MM-DD`) and a title.
2. What was done and why.
3. For **every** command: the command, what each part does, why it was needed, what the output meant.
4. Any error: the exact message, its root cause, and the fix.
