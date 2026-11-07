# UPGRADING.md: the version-to-version upgrade ledger

Adopting the methodology records a template revision in `.host`. The
template then moves on, and an adopted repo must **upgrade** across the revision
span. The upgrade re-applies spine doc changes *and* the **structural migrations** the span
introduced (a re-embedding of the software, a tool bump). A `git diff` of the
template shows the prose; it does not say "convert the submodule" or "untrack a
symlink". This ledger does.

Apply every entry below whose revision is **newer** than your stamp.
`host-lifecycle upgrade <dir>` prints exactly those, decided by git ancestry
against this template, so same-day revisions order correctly. Fetch the template
to the target revision first; then apply the list and re-stamp. Each entry is
keyed by the template revision at which its action became required.

[upgrade "8c28e33"]
    title    = Software is a bare store with worktrees (call/0004)
    action   = Convert the embedded gitlink submodule to a bare store + worktrees (see the `host` repo, converting an existing submodule): preserve the pin, de-register the gitlink, write .host-software, gitignore the trees, then `host-lifecycle software --materialize`.
    requires = host-lifecycle v0.3.0

[upgrade "325f2cf"]
    title    = Worktree-absence coherence (call/0005)
    action   = Untrack artifacts that depend on the worktree (skill symlinks into the software path); gitignore them and recreate after materialize. Keep an un-materialized CI job green. `host-lifecycle software --check` must report no HAZARD.
    requires = host-lifecycle v0.3.1

[upgrade "71d12a8"]
    title    = Coherence generalized to tool submodules (call/0005)
    action   = Re-run `host-lifecycle software --check` (now flags any tracked symlink whose target is not tracked here, not just software-worktree paths). Untrack any flagged tool-skill symlinks and generate them instead (the link-skills.sh pattern); keep them gitignored.
    requires = host-lifecycle v0.4.1

[upgrade "bbbfdc3"]
    title    = Reserve agentic-host for the meta repo; stamp is `.host`, scaffold is `host-template`
    action   = Rename your `.agentic-host` stamp to `.host`. Re-point your `template-agentic-host` submodule and its URL to `host-template`. A repo that adopts the methodology is "an agentic project" (e.g. `agentic-acme`); `agentic-host` now names only the meta repo.
    requires = host-lifecycle v0.5.0

[upgrade "7ae93cd"]
    title    = Publish via `host-lifecycle book` (the canonical doc-site publisher)
    action   = Replace any hand-rolled mdBook generator/SUMMARY with `host-lifecycle book .`; it writes book.toml (src = "docs", never ".") + docs/ in lifecycle order, renders specs, and emits a Where stub from .host-software. Run `host-lifecycle book . && host-lifecycle book --check .` before `mdbook build` (see .github/workflows/site.yml); gitignore the generated book.toml/docs/.
    requires = host-lifecycle v0.6.1

[upgrade "6db01f3"]
    title    = Anti-ouroboros: call/ is for the software, methodology lives in the spine
    action   = The methodology is owned by the spine (copy-at-version), not your call/. In a single dedicated commit, set `Status: superseded by the spine` on every accepted call/ decision that merely restates a methodology rule now settled upstream (leave the file in place, since MADR records are immutable). Add a `Scope:` header to each remaining accepted decision. Do not treat any host/management repo's top-level instance rooms as normative. `host-lifecycle validate <call-dir>` now fails an accepted decision missing `Scope:` or declaring `Scope: methodology`.
    requires = host-lifecycle v0.7.0

[upgrade "07025a7"]
    title    = book publisher v0.7.1: nested specs + retired-decision Archive
    action   = Bump your pinned `host-lifecycle book` revision to v0.7.1. Two rendering changes follow on the next build: specs nested in `spec/<topic>/` now render (previously dropped), and decisions whose MADR `Status:` is superseded/deprecated/rejected move into a trailing "Archive / Record" section (banner + nav-label suffix) instead of shipping as current chapters. The record signal is `Status:` only; `.host-lintignore` does not affect the book.
    requires = host-lifecycle v0.7.1

[upgrade "e3b174d"]
    title    = Reproducible builds are the production anchor
    action   = Record build provenance in `.host-software` per component: `build` + `toolchain` (the deterministic recipe), `deploy` (which line ships), and `artifact = <worktree-path> <sha256>`. Add a CI job that runs `host-lifecycle software --verify-build` (rebuild from the pin; fail unless the artifact reproduces); see the reference `.github/workflows/reproducible-build.yml`. Software initiated under the methodology must reproduce. Pre-existing software not yet reproducible may carry `repro-exempt = call/NNNN` citing a software-scoped case decision; the exemption is retired as it converges and is never available to greenfield software.
    requires = host-lifecycle v0.8.0

[upgrade "c137567"]
    title    = Per-platform builds for multi-platform software
    action   = For a component whose one source pin ships on several platforms, replace the flat single-build fields with one `[build "<name>" "<platform>"]` subsection per platform under its `[software "<name>"]` stanza, each with its own `build`/`toolchain`/`artifact`/`deploy` (and optional `repro-exempt`) plus an `attest-host` naming the OS (`linux`/`windows`/`macos`) that reproduces it. `host-lifecycle software --check`/`--verify-build` then attest each build only on its `attest-host`, skipping foreign-host builds rather than failing. Single-platform components need no change: the flat form stays valid.
    requires = host-lifecycle v0.9.0
    independent = true

[upgrade "d3dc5ed"]
    title    = --check artifact mismatch is a note, not a failure
    action   = Bump your pinned `host-lifecycle` revision to v0.9.1. `software --check` no longer hard-fails when a present artifact's hash differs from the recorded canonical hash (a local-toolchain build legitimately differs); it prints a `note` instead, the way `--install-hooks` already does. A match still reports `verified`; `--verify-build` (the container/CI lane) remains the reproducibility proof. No recipe change is required; this only removes a dev-box false failure.
    requires = host-lifecycle v0.9.1
    independent = true

[upgrade "b6232a5"]
    title    = Specs live with the software, not the host plan tree
    action   = Move any behaviour (.allium) or timing (.tla) specs out of the host's `plan/<milestone>/spec/` and into the software repo, beside the code they constrain. Add the verification lane to the *software's* CI, not the host's: allium gated with both `allium check` and `allium analyse` (install `allium-cli@3.4.2`; both exit non-zero on any error or warning), and specula/TLC (`tla2tools v1.8.0` on a Temurin `21` JDK). Remove the host's spec copies and its specula workflow; leave a forward note in the affected milestone. The host `plan/<milestone>/` now references a spec by path and software pin rather than containing it.
    requires = host-lifecycle v0.9.1

[upgrade "c771d60"]
    title    = Verification lanes are mandatory when a spec of their kind exists
    action   = Wire the lane tools you use as submodules and generate their skills (gitignored) with `link-skills.sh`: `tools/allium` (+ its elicit/distill/tend/weed/propagate skills) for any `.allium`, `tools/specula` for any `.tla`. Author and maintain `.allium` specs THROUGH the skills, not by hand. In the *software* repo's CI, gate each `.allium` with `allium check` + `allium analyse` + `allium plan` (install `allium-cli@3.4.2`; both check and analyse exit non-zero on any error or warning) and discharge the `plan` test obligations with the suite; TLC-check each `.tla` (`tla2tools v1.8.0` on Temurin `21`). The lane is conditional (TLA+ stays optional until a `.tla` exists, allium until a `.allium` exists), but a spec present without its full lane is a defect, not a choice. Do not treat the lanes as reference decoration.
    requires = host-lifecycle v0.9.1
    depends  = b6232a5

[upgrade "b8c54fc"]
    title    = The spec-lane MUST is enforced by software --check
    action   = Bump your pinned host-lifecycle to v0.10.0. `host-lifecycle software --check` now raises a HAZARD when a materialized component carries a `.allium` spec with no CI workflow running `allium check` + `allium analyse`, or a `.tla` with no TLC lane (`tlc2.TLC`/`tla2tools`). Wire the missing lane (per the previous entry) so --check is clean; an un-materialized worktree is skipped.
    requires = host-lifecycle v0.10.0
    depends  = c771d60

[upgrade "821a216"]
    title    = Allium plan obligations must be dispositioned per component
    action   = For each `.allium`, add a sibling `<spec>.obligations` manifest that dispositions every obligation `allium plan` derives, one of `test:<name>` (a named test discharges it), `structural` (the check/analyse lane covers it), or `waived: <reason>`. Run `host-lifecycle obligations <spec> --tests <dir>` in the software's CI (it fails on any undispositioned/stale obligation or absent test ref). Bump host-lifecycle to v0.11.1, where `software --check` also HAZARDs a `.allium` with no `.obligations` manifest.
    requires = host-lifecycle v0.11.1
    depends  = b6232a5 c771d60

[upgrade "f62d766"]
    title    = Lifecycle phases are an unconditional MUST, driven by host-lifecycle skills
    action   = Bump tools/host-lifecycle and run link-skills.sh so the phase skills (classify, adopt, embed, remap, verify, publish, upgrade) appear under .claude/skills/ alongside the allium/specula skills. Operate the methodology through these phases and their commands, never ad-hoc; the phases cover scaffolding, embedding, migration, verification, publishing, and upgrading. Unlike a verification lane, this is unconditional: there is no opt-out, and hand-operating any phase is a defect.
    requires = host-lifecycle v0.11.1
    independent = true

[upgrade "0e83e3f"]
    title    = Tag every release (a version bump MUST carry a matching vX.Y.Z tag)
    action   = Audit your tools and software for version bumps that were never tagged (`git tag` vs the manifest `version`); back-fill an annotated `vX.Y.Z` tag at each bump commit and push it. From now on, every version bump is committed with its matching tag, pushed alongside; the tag is the release a `v*` CI workflow builds. Do not re-pin `.host-software` or a tool pointer to a version-bumped commit that has no matching tag.
    requires = host-lifecycle v0.11.1
    independent = true

[upgrade "ae1e688"]
    title    = Never adopt a software repository in place
    action   = Bump your pinned host-lifecycle to v0.12.0 and re-run the classify phase as the first step of any adoption. `host-lifecycle classify <dir>` now refuses (exits non-zero, prints the embedding steps) when the target is itself a software repository (a root build manifest (`Cargo.toml`, `package.json`, `go.mod`, `pyproject.toml`, …) with no `.host` stamp and no `.host-software` recipe) instead of printing a case letter. A host is a separate meta-repo; the software is embedded as its Where room. If you previously adopted a methodology host directly on top of a software repo, split them: move the code into a bare store with worktrees recorded in the host's `.host-software`, so the host root carries only the rooms and config.
    requires = host-lifecycle v0.12.0
    independent = true

[upgrade "7de7cb1"]
    title    = Materialized worktrees must live under the host root
    action   = Bump your pinned host-lifecycle to v0.13.0. Audit `.host-software` for any worktree whose path escapes the host root (an absolute or `..`-climbing `worktrees`/`worktree` entry, or a Where-room worktree materialized at a disjoint external path with no in-structure handle). Bring each under the root: for a store that must live off-tree (another filesystem or platform), record it on the parallel line as `worktree = <dir> <branch> <pin> store=<path> [host=<os>]` and re-run `software --materialize`, which realises the store at `<path>` and the in-tree `<dir>` as a symlink/junction to it. `software --check` now HAZARDs an escaping path and a `store=` line whose in-tree handle is missing or does not resolve to the store; `host=` gates a line to one OS so a foreign-OS CI skips it rather than failing.
    requires = host-lifecycle v0.13.0
    independent = true

[upgrade "3f7c065"]
    title    = Honest partial upgrades: the applied-set stamp model
    action   = Bump your pinned host-lifecycle to v0.14.0. The `.host` stamp now records what is applied as a `baseline` ledger entry (every entry at or before its position in this file counts applied) plus an optional `applied` set of out-of-order entries, keyed by ledger position, never git ancestry. Your first `host-lifecycle upgrade` migrates a legacy single-`revision` stamp once (derives the baseline; no manual edit). Thereafter: `upgrade` lists pending by position, `upgrade --next` prints the single next safe action, and you record an applied entry with `host-lifecycle upgrade --record <id>` (id, unambiguous prefix, or ledger ordinal), which validates the id, refuses if a `depends` is unapplied, runs the entry's `verify` post-condition or requires `--unverified call/NNNN`, and appends an append-only claim. Never hand-edit the stamp. A late `independent` entry may be cherry-applied without an earlier unrelated one (deferred entries stay pending and re-list, so a forgotten or premature record can never hide owed work); `upgrade --advance` compacts a contiguous applied run into the baseline; `software --check` re-checks every recorded claim.
    requires = host-lifecycle v0.14.0
    independent = true

[upgrade "4a98d92"]
    title    = Deeper verification rungs: Apalache (symbolic), TLAPS (proof), Kani (code-conformance)
    action   = Bump your pinned host-lifecycle to v0.15.0. The verification ladder gains opt-in deeper rungs above the bounded lanes, driven by a referenced `tools/host-prove` submodule (wire it and run `link-skills.sh` only if you use a rung; its `apalache-symbolic`, `tlaps-proof` and `kani-conformance` skills turn each verifier into a one-line verdict). An obligation may now be dispositioned `kani:<harness>`, `apalache:<inv>` or `tlaps:<theorem>` instead of `test:`/`structural`/`waived:`, since a proof discharges it for all inputs/parameters; `host-lifecycle obligations <spec> --prove <dir>` validates that the named proof exists. Declaring a rung obliges its CI lane: `software --check` now HAZARDs an obligation that declares `kani:` with no `cargo kani` lane, `apalache:` with no `apalache-mc` lane, or `tlaps:` with no `tlapm` lane. Nothing is required until you declare a rung, and bare `.tla`/crate presence never activates one. Route a parametric or unbounded `.tla` invariant to Apalache/TLAPS, and a code-conformance claim to your language's verifier (Rust uses Kani); prefer byte/char-level Kani targets (`str::split`/`Vec` blow CBMC up). Verifiers install from official prebuilt binaries pinned by version + SHA256; no Docker.
    requires = host-lifecycle v0.15.0
    depends  = b6232a5 c771d60
    verify   = host-lifecycle obligations 2>&1 | grep -q -- --prove

[upgrade "a22704e"]
    title    = Self-referential software is excluded from the hygiene lane, not bypassed
    action   = Bump your pinned host-lifecycle to v0.15.1 (it fixes the first-upgrade breakage: `adopt` now registers the `host-template` submodule, the missing-template error remediates, and the `upgrade` skill matches the applied-set model). If your software detects the patterns the hygiene lane flags (a linter, parser, validator, grammar tool), it embeds them in test fixtures, docs and sometimes source, the legitimate self-reference the git hook would block. Exclude that corpus through `.host-lintignore` (host-lint v0.4.1+ honors it in the per-file hook scan, not only the `--all` walk), validated file-by-file so no real tell hides among the examples; keep ordinary source scanned (reword an example comment rather than mute the file). Never `--no-verify` past the gate to land a fixture; that silently defeats the lane. Finally, keep the template's own `tools/host-lifecycle` pin at or above the maximum `requires` in this ledger, so the pinned tool can actually run the ledger it ships.
    requires = host-lifecycle v0.15.1
    independent = true
    verify   = grep -rqs "Self-referential software is excluded" host-template/CLAUDE.md

[upgrade "897ce0d"]
    title    = Sound discharge by re-derivation (`call/0018`) + the LEXICON provenance allowlist
    action   = Bump your pinned host-lifecycle to v0.18.1, host-lint to v0.6.0, and (if you run a deeper rung) host-prove to v0.2.0. A rung obligation is now discharged by RE-DERIVATION, not name-presence: `host-lifecycle obligations <spec> --rederive <dir>` re-runs each `kani:`/`apalache:`/`tlaps:` rung through host-prove in its recorded pinned toolchain and requires a PASS at the declared bound (AVAILABLE != DISCHARGED). The offline `--prove` check stays, honestly a name-presence lint. Add the cheap offline staleness signal by declaring `inputs=<files>` on a rung and recording `<manifest>.digests` with `--rederive --record-digests`; a later offline run reports STALE if the proven inputs drift without a fresh re-derivation. Enforcement is project-pluggable (a required check, any CI, a pre-push hook, or the operator's verify phase): no keys, no CI lock-in; it generalizes the reproducible-build re-derivation so that proofs are re-derived the way artifacts are. For the hygiene lane, declare legitimate tell-shaped tokens in a `LEXICON` (each the full contextual phrase, masked; a tracker reference carries its URL); `host-lifecycle adopt` seeds a comment-only scaffold. Because a sound escape now exists, the identifier/reference tier may escalate warn to flag via a committed `host-lint: strict` directive, and `host-lint: jira-key PROJ` opts a project key into citation-gating. Curate with `host-lint lexicon add` (it refuses a master key, a laundered tell, or an un-cited reference); `host-lint lexicon --check-urls` re-derives URL liveness in a network lane.
    requires = host-lifecycle v0.18.1
    depends  = 4a98d92
    verify   = grep -rqs "discharged by re-derivation" host-template/CLAUDE.md

[upgrade "da000aa"]
    title    = Box irreducible literal citations in a host-lint:ignore fence
    action   = Bump your pinned host-lint to v0.7.0. The hygiene lane gains a per-block escape for a document that must reproduce a tell verbatim: a fenced code block tagged `host-lint:ignore` (markdown only). Its lines are skipped by the naming scan while the rest of the file stays linted, and a regular code block or inline backticks stay scanned so a tell cannot be laundered by quoting it. Reserve it for an irreducible literal citation (an old-name remap table, a frozen dated review citing another document's numbered steps); reword a pedagogical example or a document's own ordinal label into content, and path-exclude (`.host-lintignore`) only the immutable record (the append-only memory log, dated review artifacts) and the self-referential corpus. This loosens, never widens, the gate: it replaces blanket path-exclusion of editable docs with in-file, per-block, still-audited boxing.
    requires = host-lifecycle v0.18.1
    independent = true
    verify   = grep -rqs "boxed in the file, not path-excluded" host-template/CLAUDE.md

[upgrade "617e420"]
    title    = Lifecycle manifest, and every phase emits a receipt
    action   = Bump your pinned host-lifecycle to the v0.18.1 build that ships `manifest`/`receipt`/`release`. The lifecycle phases (their order, modality, command and the evidence each carries) now live once in a tool-readable `lifecycle.manifest` at the template root (the CLAUDE.md/STRUCTURE.md prose point at it instead of re-typing the order), and a `release` phase is added (the strict, tool-carried release: verify, build in the recorded toolchain, re-derive the artifact hash, re-pin, tag, receipt). The rule changes from "every phase runs, no opt-out" to **every phase emits a receipt**: `host-lifecycle receipt --record <phase> [--component <c>] --disposition done|skip` writes an append-only `.host-receipts`, and `host-lifecycle software --check` now HAZARDs any manifest phase with no receipt, re-verifying each `done` by the manifest's closed `recheck =` (never the receipt's own say-so). Modality is first-class: a `conditional-on-Where` phase is tool-computed `n-a` where the project has no Where room, a `recurring-per-component` phase (embed, release) is receipted once per component, and a protected core (`verify`, `skippable = false`) refuses a skip. Back-fill a receipt for each phase your project has already done; `host-lifecycle manifest <path>` prints the whole lifecycle at a glance.
    requires = host-lifecycle v0.18.1
    independent = true
    verify   = grep -rqs "every phase emits a receipt" host-template/CLAUDE.md

[upgrade "0cd6b0a"]
    title    = The Where room uses the nested software/<name>/<branch> layout
    action   = Bump your pinned host-lifecycle to v0.19.0. The Where room now materializes under `software/<name>/`: the bare store at `software/<name>/.git` and each worktree keyed by branch at `software/<name>/<branch>/` (the canonical worktree is the recorded `branch`, default `main`, checked out at the pin), replacing the old root-scattered `<name>/`, `<name>.git/`, `<name>.<line>/`. Migrate, in order: (1) replace the per-component `.gitignore` triplets with a single `/software/` entry; (2) remove the old root-scattered worktrees and bare stores (commit or stash any uncommitted parallel-worktree work first, since re-materialize is destructive); (3) run `host-lifecycle software --materialize .` to realise the new tree; (4) re-run `link-skills.sh` and re-point any software skill link at `software/<name>/<branch>/`; then `host-lifecycle software --check .` must be clean. The `worktree =` recipe line drops its leading `<dir>` token (the path now derives from the branch: `worktree = <branch> <pin> [store=<path>] [host=<os>]`), `worktrees =` is a branch list, and an optional `branch =` sets a non-`main` canonical branch. Operate on one component (or one branch worktree) with `software --item <name>[@<branch>]`. `software --check` also HAZARDs a dangling generated skill link now. A development host that authors a host-* tool embeds it as its own Where component rather than referencing its own source as a submodule (the reference-don't-vendor carve-out).
    requires = host-lifecycle v0.19.0
    independent = true
    verify   = grep -rqs "the producer of a tool embeds it" host-template/CLAUDE.md

[upgrade "950fbd6"]
    title    = Prose hygiene is an ongoing hygiene-lane rule with a receipt
    action   = Treat the prose audit as a STANDING part of the hygiene lane, not a one-time pass. `host-lint --prose` (host-lint v0.7.0+) flags the LLM-slop prose tropes that tropes.fyi names (decoration dashes and arrows, tricolons, hypophora, and the rest) in authored docs. Clean every authored doc to ZERO prose tropes (reword to plain prose, the same bar as naming tells), then wire it into the receipts mechanism: the `verify` phase applies `host-lint --prose` and generates a receipt, and `host-lifecycle software --check` re-verifies that receipt by re-running `--prose` (add it to the `verify` phase `recheck =` in `lifecycle.manifest`), re-opening any regressed doc as a HAZARD. `MEMORY.md` is the agent's append-only working memory and is excepted from both the naming and prose audits via `.host-lintignore`, never rewritten.
    requires = host-lifecycle v0.19.0
    independent = true
    verify   = grep -rqs "Prose hygiene is the same lane" host-template/CLAUDE.md

[upgrade "ecce498"]
    title    = Hermetic builds via a pinned dependency bundle
    action   = Bump your pinned host-lifecycle to the v0.20.0 build that ships the `deps-bundle` recipe field and the offline `--network none` build. A component that ships static or self-contained release binaries MUST be able to reproduce them offline from pinned inputs, never from a network fetch at build time. Vendor the dependency layer once and publish it as a reusable, versioned, hash-pinned downloadable release bundle (the pattern `pgs-release` uses for its prebuilt sysroot), then record it per component as `deps-bundle = <url> <sha256>` in `.host-software`. `host-lifecycle software --verify-build` and `release` perform the one controlled, pinned download, verify the sha (provenance), stage the vendored sources, and build under `--network none` (egress). The producer commits a `deps-bundle.lock` as the single source of truth, and `software --check` HAZARDs a `deps-bundle` pin that has drifted from it. A component that genuinely cannot vendor offline (a network-fetching `build.rs`, a non-Rust toolchain) may carry `hermetic-exempt = call/NNNN` citing a software-scoped case decision, the same escape shape as `repro-exempt`; the exemption is never available where offline vendoring is feasible.
    requires = host-lifecycle v0.20.0
    independent = true
    verify   = grep -rqs "reproduce them offline from pinned inputs" host-template/CLAUDE.md

[upgrade "27d815b"]
    title    = The hygiene grammar grows by reflective practice
    action   = Bump your pinned host-lint to v0.9.0, which flags a positional reference to a milestone checklist item (the "box N" / "boxes N-M" / "steps N-M" shape), the same ordinal-by-position tell as a numbered name. Adopt the living-grammar doctrine: the shared tell corpus is incomplete and grows by reflective practice. Discovery is mechanical-first, a sweep of history and recent work for a recurring shape the lane misses, prompted at the verify gate before a milestone closes and at adoption, with the agent assisting rather than leading. The operator validates whether a surfaced shape is a genuine tell or legitimate domain vocabulary, by one test: is the shape a property of how models segment work, or of this project's own domain? A confirmed tell is proposed upstream to the shared grammar the lane consumes (a naming tell to host-lint, a prose trope to host-grammar), gained on the next bump; a legitimate tell-shaped token stays in the per-project `LEXICON`; the project that finds a tell does not edit the shared source itself. Reword by default; box or declare an irreducible citation; declare the numeral-free contextual prefix for a genuine quantity; reserve a graduation for the residue. A later grammar bump that flags a live doc is reworded, and a frozen record is boxed.
    requires = host-lifecycle v0.20.0
    independent = true
    verify   = grep -rqs "grows by reflective practice" host-template/CLAUDE.md

[upgrade "e280a8d"]
    title    = The verify recheck re-runs the prose audit, so the gate enforces prose hygiene
    action   = Bump your pinned host-lifecycle to v0.22.0, which adds `host-lifecycle prose <dir>`, host-lint's `--docs` prose audit run in-process so the gate needs no host-lint on PATH (a development host whose host-lint is embedded Where software still runs it). The `verify` phase `recheck =` in `lifecycle.manifest` now chains `host-lifecycle prose .` after `validate`, so `software --check` re-verifies the verify receipt by re-running the prose audit and re-opens any doc that regressed to slop as a HAZARD. This enforces the standing prose-hygiene rule the spine already states; before it the recheck ran only `validate`, so a prose regression slipped past the gate.
    requires = host-lifecycle v0.22.0
    independent = true
    verify   = grep -rqs "host-lifecycle prose" host-template/lifecycle.manifest

[upgrade "ac32d1c"]
    title    = Re-home the receipts family, tool-driven
    action   = Bump your pinned host-lifecycle to v0.23.0 and run `host-lifecycle migrate-receipts .` (one command, never hand-edited). It moves the applied-set out of `.host` into `.host-receipts` and splits the operational receipts (classify, embed, remap, verify, publish, release) out to `.host-lifecycle-receipts`; adopt and upgrade stay in `.host-receipts`. The binary auto-migrates on read, so the gate stays green across the boundary and an un-migrated project is still read correctly. A receipt is methodology-version (`.host-receipts`) only for adopt and upgrade; every other phase host-lifecycle runs is operational (`.host-lifecycle-receipts`). The old-layout reader is permanent backward compatibility, not a one-time shim.
    requires = host-lifecycle v0.23.0
    independent = true
    verify   = test -f .host-lifecycle-receipts

[upgrade "d5a0034"]
    title    = Reflective practice grows in two arms: gather forward, reconcile backward
    action   = Bump your pinned host-lifecycle to v0.24.2, which adds `host-lifecycle reconcile <dir>` and wires the reconcile step into the `upgrade`/`adopt`/`verify` skills. Adopt the widened doctrine: an agent perceives neither the register it emits nor the restatements its own change stales, so reflective practice runs in two arms under one principle. The first arm, gather (unchanged), is forward: emergent tells in the corpus, a confirmed tell graduates upstream, cadence-driven. The second arm, reconcile (new), is backward: the project's own restatements of methodology (its room map, tool family, verification model, recorded Where layout), a confirmed drift fixed locally and never propagated. Prefer pointing at the spine over restating it; a restatement that must stay carries an inline `<!-- host-reconcile: KIND -->` annotation declaring an assertion `host-lifecycle reconcile` checks against a source of truth (the host-* family list and the verification-ladder drivers the lifecycle manifest records, the fixed `software/` and `plan/` layout), with kinds `family`, `verification`, `where-root`, `spec-path`. The trigger is conditional and host-aware: a `restates =` field on an UPGRADING entry marks a drift-capable move so the upgrade skill re-reads the named kinds, adoption runs the full reconcile once, and for a development host that authors its own spine changes the verify gate is the binding trigger (the verify recheck now chains `host-lifecycle reconcile .`). Disposition is three-way (reword a live restatement, box a frozen citation, forward-correct an immutable record). A sibling check: `host-lifecycle validate` now HAZARDs an accepted `call/` decision whose `Scope:` names `host-template`, since its rule is spine-resident and belongs superseded there.
    requires = host-lifecycle v0.24.2
    independent = true
    verify   = grep -rqs "Two arms run under this one principle" host-template/CLAUDE.md

[upgrade "7be692f"]
    title    = Reconcile evolves to concept-as-URI; the lifecycle manifest is phases-only
    action   = Bump your pinned host-lifecycle to v0.25.0 and move to this host-template revision together (a partial bump leaves the old manifest stanzas under the hardened `manifest --check`). The lifecycle manifest is now phases only; a project's own facts live in its `.host-software`. Define each methodology concept once at a `{#id}` anchor on a heading (for example `## Components {#components}`) in a doc of your choice, and point at it elsewhere with `[text](FILE#id)`; reconcile runs link-integrity, declared-anchor, and coverage over your docs. The concepts: `components` (your host-* tools, the `[software]` members of `.host-software` minus a single-file front door marked `front-door = true` if you have one), `verifiers` (your verification drivers, named on a `drivers = ...` line under a `[verification]` stanza you add to `.host-software`, for example a `[verification]` stanza whose line is `drivers = host-lint allium specula host-prove`), `software-root` (where your software lives, `software/`), and `spec-home` (where your specs live, with the software). Each home that lists a set must name the whole set; coverage flags an omission. Convert each surviving inline `<!-- host-reconcile: KIND -->` annotation by replacing its enumeration and comment with a single such link. You may migrate gradually: the inline annotations keep working, warned, until a later revision retires them. See the reconcile section in `CLAUDE.md` for the full rules.
    requires = host-lifecycle v0.25.0
    independent = true
    verify   = grep -rqs "rejects a project-fact stanza" host-template/CLAUDE.md

[upgrade "2229dbb"]
    title    = In-plan tasks are a receipted dependency graph
    action   = Bump your pinned host-lifecycle to v0.26.0 and move to this host-template revision together. Each entry under a milestone's `## Build sequence` becomes a task: an anchored `### ` heading ending in `{#anchor}`, keyed `plan/NNNN#anchor`. A task declares its prerequisites with `- depends: #anchor` (or a cross-milestone `plan/NNNN#anchor`; omit the line for the previous task, the linear default), its check with `- verify: <command>` (mechanical) or `- verify: attested <call/NNNN | operator>`, and the files a mechanical verify covers with `- inputs: <paths>`. Record a receipt for each task with `host-lifecycle tasks --record <plan/NNNN#anchor> --disposition done|skip` (the tool reads the task's own `verify`/`inputs`, so you never re-type them); `software --check` then HAZARDs a task with no receipt, a `done` whose inputs drifted or whose citation does not resolve, a `skip` without a resolvable `call/NNNN`, and an orphan receipt whose task was renamed or removed. Declare only what must finish first; the tool derives what runs in parallel, and a coordinator parallelizes only resource-isolated workers. Migrate gradually: a plan with no anchored `### ` task is untouched. See the task-graph section in `CLAUDE.md`.
    requires = host-lifecycle v0.26.0
    independent = true
    verify   = grep -rqs "in-plan tasks are receipted nodes" host-template/CLAUDE.md

[upgrade "ba86125"]
    title    = The entrance check holds a self-contained document to the spine
    action   = Bump your pinned host-lifecycle to v0.29.0 and move to this host-template revision together. A document read out of context cannot point at a definition, so the entrance check holds it by coverage and generation, reconcile's standalone sibling. Declare one entrance, a global singleton, in an `[entrance]` stanza in `.host-software` naming the `member` it belongs to (set apart from `components`), the `document` within that member (default `README.md`), and the concepts it `restates` (`true` for every concept, or a named subset of `phases`, `tools`, `stamp`). `host-lifecycle entrance --check` then holds that document complete against the declared concepts. If you marked a single-file front door with the legacy `front-door = true` or `entrance = true` on its `[software]` member, replace it with an `[entrance]` stanza naming that member; the legacy marker is still accepted, warned, until a later revision retires it.
    requires = host-lifecycle v0.29.0

    verify   = grep -rqs "entrance check is reconcile's standalone sibling" host-template/CLAUDE.md

[upgrade "de8a517"]
    title    = The legacy per-member entrance marker is retired
    action   = Bump your pinned host-lifecycle to v0.30.0 and move to this host-template revision together. The legacy per-member entrance marker is retired: a `front-door = true` or `entrance = true` on a `[software]` member is now a loud error, not silently accepted. Replace any such marker with an `[entrance]` stanza naming that member (the `member`, an optional `document` with default `README.md`, and `restates`); see the entrance section in `CLAUDE.md`. A project with no single-file entrance carries no such marker and needs no change.
    requires = host-lifecycle v0.30.0

    verify   = grep -rqs "The legacy per-member marker is retired" host-template/CLAUDE.md

[upgrade "e068828"]
    title    = The generated book moves under mdBook/, freeing docs/
    action   = Bump your pinned host-lifecycle to v0.30.2 and move to this host-template revision together. `host-lifecycle book` now writes its generated mdBook source to `mdBook/src/` and the built HTML to `mdBook/out/`, with `book.toml` kept at the repo root, so `mdbook build` still runs from the root. This frees `docs/` for your own authored documentation. Update your `.gitignore`: replace the `/docs/` and `/book/` lines with a single `/mdBook/` line, keeping `/book.toml`. Regenerate the site with `host-lifecycle book .`, then remove the stale generated `docs/` and `book/` trees, which held only generated output under the old layout (`git clean -fd docs book` reaches them once they are no longer ignored). If your `.github/workflows/` publishes the site, point the publish step at `mdBook/out` in place of `book`. A project that has not yet published a site carries no generated `docs/`, so it needs only the gitignore and workflow change before it first runs `book`.
    requires = host-lifecycle v0.30.2
    independent = true
    verify   = grep -rqs "mdBook/src" host-template/STRUCTURE.md

[upgrade "6174996"]
    title    = A declared rung obliges a runnable re-deriver, not just a present CI lane
    action   = Bump your pinned host-lifecycle to v0.31.0 and move to this host-template revision together. `software --check` now HAZARDs a declared deeper rung (`kani:`/`apalache:`/`tlaps:`) whose shared re-deriver, host-prove, does not run, beside the existing no-CI-lane HAZARD, because a re-derivation that cannot run leaves the rung undischarged however complete the CI config reads. So install host-prove on PATH wherever the gate runs: your local setup and the CI that runs `software --check` (`cargo install --git https://github.com/connollydavid/host-prove --rev <its pin>`). A project that declares no deeper rung carries no host-prove requirement and needs no change. And earn the digest a rung records through `host-lifecycle obligations <spec> --rederive <crate-root> --record-digests`, which re-runs the proof and records only on a pass, in place of a hand edit, so a fresh digest stands for a passing re-derivation on the current inputs.
    requires = host-lifecycle v0.31.0
    independent = true
    verify   = grep -rqs "a re-deriver that runs" host-template/CLAUDE.md

[upgrade "46a1fd2"]
    title    = A verification lane reports clean only after it performs its check
    action   = Bump your pinned host-lifecycle to v0.32.0 and move to this host-template revision together. The obligation-discharge check now verifies an `exercises=<symbol>` link rather than only that a `test:` name resolves. Add to each behavioural obligation a link naming a function the discharging test drives, and run `host-lifecycle obligations <spec> --tests <dir> --strict-discharge` where the gate runs. The strict mode is opt-in, so a tool bump leaves your ladder green; the reject names the test and the symbol it is missing. Do not relabel a behavioural obligation `structural` to dodge it, and give every `waived:` a real reason. Separately, `software --verify-build` is now three-state: it prints its clean line only when a build was verified and none was UNVERIFIABLE, and it exits non-zero on an in-scope build it could not run (no container runtime, or no toolchain pin), so a runtime-less CI that relied on its exit 0 must gain a runtime or scope that build out. A project whose obligations are all `structural` carries no `exercises=` link and needs only the verify-build change.
    requires = host-lifecycle v0.32.0
    independent = true
    verify   = grep -rqs "reports clean only after it performs its check" host-template/CLAUDE.md
