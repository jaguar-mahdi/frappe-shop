# Frappe Shop Constitution

## Core Principles

### I. Extend, Never Modify

- Source code of `frappe`, `erpnext`, `payments` and `webshop` MUST NOT be edited.
- Every customization MUST live in the `frappe_shop` app and use extension mechanisms only:
  Custom Fields exported as fixtures, hooks, and overrides.
- A change that cannot be made by extension MUST be raised with the maintainer before any work starts.

Rationale: upstream apps stay upgradeable, and every customization is versioned in one repository.

### II. Pull Requests, Green CI, Conventional Commits, Semantic Versioning

- Every change MUST reach `main` through a Pull Request. Direct pushes to `main` are not allowed.
- A Pull Request MUST NOT be merged unless the required checks pass: `Server`, `Frappe Linter`,
  and `Vulnerable Dependency Check`.
- Commit messages and Pull Request titles MUST follow Conventional Commits.
- Releases of the app MUST follow Semantic Versioning (`MAJOR.MINOR.PATCH`).

Rationale: every change is reviewed and checked the same way, and the history explains itself.

### III. Every Feature Ships With a Test

- Every feature MUST include at least one automated test that runs in CI.
- A feature without a passing automated test is not done.

Rationale: tests prove a feature works and keep it working after later changes.

### IV. Security

- Secrets MUST NOT be committed. This includes passwords, API keys, tokens, and the content of
  `site_config.json`. The repository is public.
- Dependency and security scans (`Frappe Linter` Semgrep rules and `Vulnerable Dependency Check`)
  MUST stay enabled and required. They MUST NOT be removed, skipped, or made optional.

Rationale: a public repository exposes anything committed, and scans catch known risks early.

### V. Simplicity

- Each change MUST use the smallest solution that meets its goal.
- The store MUST NOT integrate a real payment gateway.

Rationale: a small scope is easier to build, test, review, and explain.

## Platform Constraints

- Platform: Frappe Framework `version-16` with `erpnext`, `payments` and `webshop` on `version-16`.
- All project code lives in the `frappe_shop` app repository.

## Development Workflow

- Work happens on a branch named `<type>/<short-kebab-description>`, never on `main`.
- `pre-commit run --all-files` MUST pass before every push, matching CI.
- `main` accepts squash merges only, with linear history. The Pull Request title becomes the commit on `main`.
- Pull Requests are opened by the maintainer or by Claude Code. Claude Code may merge a Pull Request
  only with a squash merge after all required checks pass, and MUST NOT bypass the Ruleset (no admin
  merge, no direct push to `main`). Product decisions (features, data fields, naming,
  UX, licensing, scope) belong to the maintainer.

## Governance

- This constitution overrides other practices in this repository. `CLAUDE.md` and
  `docs/git-workflow.md` give day-to-day guidance and MUST NOT contradict it.
- Amendments are made through a Pull Request that the maintainer approves and merges. The Pull
  Request MUST state the version change and the reason for it.
- Versioning policy (Semantic Versioning of this document):
  - MAJOR: a principle is removed or redefined in a backward-incompatible way.
  - MINOR: a principle or section is added, or guidance is materially expanded.
  - PATCH: clarifications, wording, and typo fixes with no change in meaning.
- Compliance: every implementation plan MUST include a Constitution Check against Principles I–V,
  and every Pull Request review MUST confirm compliance. Any exception MUST be justified in writing
  in the plan.

**Version**: 1.1.0 | **Ratified**: 2026-11-21 | **Last Amended**: 2026-11-21
