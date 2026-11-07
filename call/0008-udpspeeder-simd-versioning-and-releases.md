# udpspeeder-simd versioning and releases

- Status: accepted
- Scope: udpspeeder-simd
- Date: 2026-08-10

## Context and Problem Statement

The fork has released v1.0.0 through v1.0.6 with no recorded versioning policy.
Every bump so far has been a patch (a fix layered on the same feature surface), cut
by tagging the fork and letting CI build the binaries. The milestone currently
planned (`plan/0001`) is the first feature addition since the fork diverged, which
makes it the first minor bump. The room has no decision that states what a minor
bump means, what the tag carries, or how the release is recorded, so the v1.1.0
release would otherwise be cut the way the v1.0.x line was: by habit, with the
reasoning living only in the tag.

`call/0006` governs reproducibility (the binaries are not yet byte-reproducible, and
the stanza carries a waiver). It does not govern versioning or cadence.

## Decision

The fork follows semantic versioning on its tags, with the release process the
v1.0.x line already established:

- A **minor** bump (from the `vX.Y` patch line to `vX.<Y+1>.0`) carries a user-visible
  feature; a **patch** bump carries a fix. The first minor bump is `v1.1.0`, cut for
  the DNS lease manager feature in `plan/0001`.
- The **tag is the release**, per the spine rule: a version bump MUST be accompanied
  by a matching annotated tag `vX.Y.Z` at the release commit, pushed alongside it.
  The tag-triggered CI job builds the artifacts from it.
- The banner `PROGRAM_VERSION` in `main.cpp` must equal the tag; the fork CI enforces
  the match on tag pushes.
- The host records each release by re-pinning the `.host-software`
  `udpspeeder-simd` stanza to the tagged commit and recording the `release` phase
  receipt for the component.

## Consequences

- Good: a future release is cut the same way, with the meaning of the bump decided
  before the tag, not after; the v1.1.0 bump has a citable decision behind it.
- Good: the release receipt ledger (currently a stale `skip` for this component)
  gains a real `done` entry once `plan/0001` ships.
- Neutral: the OpenWrt feed package bump is a separate milestone, and the fork
  release is merely its prerequisite.
- Follow-up: `call/0006` still governs reproducibility; when the build becomes
  deterministic, that waiver is retired and this decision's release-mechanics half
  stays in force.