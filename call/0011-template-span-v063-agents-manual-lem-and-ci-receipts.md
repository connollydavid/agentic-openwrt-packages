# The template span through the v0.63.0 pins: the AGENTS.md manual, the lem system, and the CI-receipt lane

- Status: accepted
- Scope: host
- Date: 2026-11-07

## Context and Problem Statement

The template moved a dozen ledger entries past the revision adopted on
2026-11-07 (the day before) and now ends at pins of host-lifecycle v0.63.0 and
host-lint v0.24.1. The span renames the operating manual to `AGENTS.md`
(`CLAUDE.md` becomes a one-line pointer), adds the `lem` pronoun system and its
enforcement lane, declares an always-loaded corpus held to a strict prose tier,
adds the reference-citation link form, turns CI lanes into receipted outcomes,
adds the push-boundary check lane, and documents the `regen` recipe key and the
reference-lane doctrine.

Two findings of the day's earlier session shaped how the span landed. First,
the exec-bit audit over-fire recorded in
[`call/0010`](0010-exec-bit-audit-over-fires-on-the-openwrt-install-idiom.md)
is fixed at v0.63.0: the audit no longer flags the OpenWrt install-macro
corpus, so the interim staged-chmod state is retired and that decision is
superseded by this one. Second, the completeness gate at v0.50.0 could not pass
on this host's dual host-lint embedding (one skill link name demanded by two
sources); v0.63.0 resolves it and `bootstrap` completes again.

## Decision

- The manual is `AGENTS.md`, renamed with history (`git mv`), carrying the
  template spine at the adopted revision plus this host's own tail (the two
  priority rules and the project specifics), and `CLAUDE.md` is the pointer.
  The corpus is declared `active-corpus = .host-corpus` naming `AGENTS.md` and
  `STRUCTURE.md`; `GOAL.md` joins it when a goal is first set.
- The ledger entry `LEM-pronoun-system` records with the unverified escape
  citing this decision: its verify greps `CLAUDE.md`, and the rename that the
  later entry `ACTIVE-corpus-and-agents-manual` performs in the same span
  leaves that name a pointer. The entry's action is satisfied; the section
  lives in the manual under its new name.
- CI receipts follow an evidence policy, recorded here so each URL can be read
  for what it is. Where a lane has a green run at the judged revision, that run
  is cited. Where the lane is PR-scoped or the component is a consumed upstream
  pin with no such run, the receipt cites the lane's most recent run in that
  repository, green or not, as the read-and-recorded evidence. Four upstream
  OpenWrt lanes (`kernel`, `label-kernel`, `label-target`, `packages`) carry
  their latest runs, which are not green on upstream's own repository; those
  receipts record that fact rather than claim health.
- Two structural gaps stay red and disclosed, because no honest receipt exists
  for either. The `packages` fork's master mirror pin declares
  `multi-arch-test-build` and `stale-bot` lanes that the fork's forge never
  registered (the workflow list carries only `flashprog.yml`), so no run URL
  exists to cite. The host `check` and `qemu packet test` lanes receive their
  first post-change runs from this session's push; their receipts follow those
  runs. An upstream proposal extending the ci judge with an absence
  disposition for consumed mirror pins is the owed remedy, in the shape of
  `call/0010`'s issue.
- The `qemu packet test` lane's standing failure is fixed in the same push:
  the feed branches renamed `net/udpspeeder-simd` to
  `net/udpspeeder-simd-snapshot`, and the lane's sparse checkout, feed symbol,
  and make target now use the snapshot names (the installed binary keeps its
  `udpspeeder-simd` name, so the binary loops are unchanged).
- The spine's task-graph example fence is tagged `host-lint:ignore` in this
  host's copy, as an interim unblock with two defects disclosed: the v0.63.0
  template mis-nests its new goal-loop section inside that example fence, and
  the example's own short anchor violates the anchor-equals-slug rule the same
  release's host-lint ships. Both fixes belong in the template; the tag is
  local only and the next spine re-apply that still carries the defect must
  re-apply the tag with it. The sixteen anchor flags over the receipted task
  anchors of `plan/0000` and `plan/0001` are left standing for the same
  reason: renaming an anchor orphans its task receipts, the open no-rename
  defect recorded upstream, so the anchors keep their identity.

## Consequences

- The host runs the declared toolchain host-lifecycle v0.63.0 and host-lint
  v0.24.1 (component pin and submodule pointer at `db4a0d20`, artifact hash
  re-derived from a fresh `--locked` build), with `.env` carrying the
  hash-verified release download.
- `call/0010`'s interim staged-chmod state is no longer needed; the worktree
  indexes are left as the gate finds them, and that decision's disposition is
  superseded by the tool fix it asked for.
- The record of the day's cross-check of the previous checkout (an untracked
  read-only `flashprog-test-packages` artifact directory kept in place, and the
  pre-rewrite originals of the udpspeeder-update work preserved as the pushed
  `archive/udpspeeder-update-pre-rewrite` branch) lives in `MEMORY.md`.
