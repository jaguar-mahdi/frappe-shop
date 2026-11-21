# Releasing

How a new version of `frappe_shop` is released. Constitution Principle II requires Semantic
Versioning (`MAJOR.MINOR.PATCH`).

## 1. Choose the version from the Conventional Commits

Look at the commits on `main` since the last tag:

```bash
git log --oneline v0.1.0..main      # e.g. for the release after v0.1.0
```

| Commits since the last release | Bump | Example |
| --- | --- | --- |
| A `BREAKING CHANGE:` footer, or `!` after the type (`feat!:`) | MAJOR | 1.4.2 → 2.0.0 |
| At least one `feat:` | MINOR | 1.4.2 → 1.5.0 |
| Only `fix:` (and `docs`, `chore`, `ci`, `test`, `refactor`, `style`, `build`) | PATCH | 1.4.2 → 1.4.3 |

While the version is `0.y.z`, the API is not considered stable. Breaking changes bump MINOR
(`0.1.0 → 0.2.0`), and everything else bumps PATCH.

## 2. Version bump PR

```bash
git switch main && git pull --ff-only origin main
git switch -c chore/release-X.Y.Z
# frappe_shop/__init__.py  ->  __version__ = "X.Y.Z"
# CHANGELOG.md            ->  move "Unreleased" items into "## [X.Y.Z] - YYYY-MM-DD"
pre-commit run --all-files
git commit -am "chore(release): X.Y.Z"
git push -u origin chore/release-X.Y.Z
gh pr create --base main --title "chore(release): X.Y.Z" --body-file <file>
gh pr checks <n> --watch
gh pr merge <n> --squash --delete-branch      # only when all required checks pass
```

## 3. Tag and GitHub Release

```bash
git switch main && git pull --ff-only origin main
gh release create vX.Y.Z --target main --generate-notes --title "vX.Y.Z"
```

- The tag is `v` + the version (`v0.1.0`). `gh release create` creates the tag on `main` when it
  does not exist yet.
- `--generate-notes` lists the merged PRs since the previous release. `CHANGELOG.md` stays the
  curated, human-readable history.
- Never move or delete a published tag. If a release is broken, publish a new PATCH version.

## 4. Release workflow (automatic)

Publishing the release triggers `.github/workflows/release.yml` (`on: release: published`):

1. It builds a Docker image with the `frappe_docker` layered Containerfile: Frappe `version-16` +
   `payments`, `erpnext`, `webshop` (`version-16`) + `frappe_shop` at the release tag.
2. It pushes `ghcr.io/jaguar-mahdi/frappe-shop:X.Y.Z` and `:sha-<commit>`. There is no `latest`.
3. The job runs in the `staging` environment, so GitHub records a deployment.

Check it:

```bash
gh run list --workflow release.yml --limit 1
gh run watch <run-id>
gh api repos/jaguar-mahdi/frappe-shop/deployments --jq '.[0] | {environment, ref, sha}'
```
