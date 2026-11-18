# CLAUDE.md

Standing rules for Claude Code in this repository. Details live in [docs/git-workflow.md](docs/git-workflow.md).

## Session start

- State an estimated time before beginning any work.
- Work only from `/workspace/development/frappe-bench/apps/frappe_shop`. Run `pwd` to confirm before any git command.
  (`/workspace/development` is a different repo, `frappe_docker`: never run git there.)

## Decisions

- Never make product decisions: features, data fields, naming, UX, licensing, scope.
  If a decision is about the product rather than the code, stop and ask.

## Git and GitHub

- Never commit or push to `main`. It is protected by a Ruleset: PR required, squash merge only,
  linear history, required checks `Server`, `Frappe Linter`, `Vulnerable Dependency Check`.
- Workflow: branch → commits → push → the user opens and merges the PR. Do not open or merge PRs (`gh` is not installed).
- Branch names: `<type>/<short-kebab-description>`.
- Commit messages and PR titles follow Conventional Commits
  (`feat`, `fix`, `docs`, `style`, `refactor`, `test`, `ci`, `chore`, `build`).
  The PR title becomes the squash commit on `main`.
- Run `pre-commit run --all-files` before every push (CI runs it with `--all-files`).

## Safety

- Use explicit commands and pinned versions; avoid `latest` where a pin is possible.
- The repo is public: never commit secrets, passwords, or `site_config.json` content.

## After every task

- Append an entry to [docs/learning-log.md](docs/learning-log.md) (format in [docs/git-workflow.md](docs/git-workflow.md#learning-log-format)).

## Communication

- Explain things to the user in Arabic; put every English term in inline code.
- Spell out every abbreviation in full the first time it appears.
