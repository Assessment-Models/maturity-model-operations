# Contributing to `maturity-model-operations`

## Change control

Changes go through a pull request with a rationale and a `CHANGELOG.md`
entry. Semver applies:

- **MAJOR** — level or band definition change
- **MINOR** — new dimension or criterion
- **PATCH** — clarifications, corrections, additional evidence examples

## Rules

1. **Do not alter level semantics without a change request.** Characteristics,
   exit criteria and evidence are the model's substantive content; changing
   them changes what the instrument measures.
2. **Band definitions are canonical upstream.** Band widths and effort
   multipliers are owned by `dea:maturity-bands-v2` in
   `technehub-labs/dea-metamodel`. Do not copy or restate them as local
   truth — reference them.
3. **References are immutable.** Every external reference (component, scale,
   dependency) must be a tag `vX.Y.Z`, a 40-character commit SHA, or a
   sha256 digest. `main`, `master` and `latest` are rejected by CI.
4. **Level 1 and Level 2 CI must be green** before merge. Level 2 resolves
   the handshake against the pinned `dea-metamodel` release.
5. **Model identity is the registration id.** The `id` in `model.yaml` must
   match the `repo_id` in the model register and the id in
   `Assessment-Models/assessment-registry`. The repository name is a
   location, not an identity.

## Registering a release

After a release is tagged, add or update the registration record under
`Assessment-Models/assessment-registry/registry/` with the immutable tag
reference. A record must not point at a repository or reference that does not
resolve — the ecosystem validator checks this.

## Licence

By contributing you agree that your contributions are licensed under the MIT
licence of this repository.
