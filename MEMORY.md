# The agent's own append-only working memory. Excluded from the naming and prose
# audits via .host-lintignore; never rewrite an old entry (correct in place with a
# dated pointer). A fresh session reads plan/, call/, and this file to continue.

## 2026-07-02 — host adopted

- Adopted `host-template` @ `565410a` for UDPspeeder-simd (case a, Shallow). Stamp
  written by `host-lifecycle adopt`; rooms `cast/ plan/ call/` scaffolded.
- Push auth: the stored git credential is the `slartibardfast` token, which had no
  push rights to `connollydavid/agentic-UDPspeeder-simd` (HTTP 403 on first dry-run
  push). The operator authorized the repo, after which `git push --dry-run` returned
  "Everything up-to-date". If a later push 403s again, surface it to the operator
  rather than retrying blindly.
- Tooling built from source with the system toolchain (rustc 1.96.1, Arch Linux).
  The methodology pins Rust 1.95.0 as the reproducible-build anchor; the local
  builds use 1.96.1, which is newer and builds clean. Record this wherever a
  canonical artifact hash is claimed.
- UDPspeeder-simd embeds as a bare store plus worktree at
  `software/udpspeeder-simd/branch_libev/` (its default branch is `branch_libev`,
  not `main`). Recorded in `.host-software` with no `deploy`/`artifact`, so it is a
  source pin with no reproducible-build claim yet (migrated software).
- host-lint is also a `.host-software` component (the gating tool): `--install-hooks`
  reads a component's `hooks` script and built `artifact` from its materialized
  worktree, so host-lint must be materialized and built for the commit gate to land.

## 2026-07-03 — gate green; runtimes installed; push auth is flaky

- The verify gate (`host-lifecycle software --check .`) is green: both components at
  pin, all phase receipts recorded, prose clean, reconcile clean. The commit-msg hook
  blocks an ordinal tell in a message (tested: `phase 1` is rejected, exit 1).
- Tooling on this machine, all under `~/.local`: `bin/host-lint`, `bin/host-lifecycle`
  (v0.35.1), `bin/host-prove` (v0.3.0), `bin/allium` (3.5.0), `jdk-21/` (Temurin
  21.0.11), `share/tla2tools.jar` (v1.8.0, sha256 237332bd). The gate needs
  `host-prove` on PATH because host-lint's own `kani:` obligations surface once it is
  materialized as a component; the cheap gate probes `host-prove --help`, it does not
  run Kani.
- Two clearance details: the toolchain HAZARD (artifact with no toolchain) is waived by
  `repro-exempt = call/0002` on host-lint (consumed tool, not reproduced here); and
  `remap` is a `skip` receipt, not `done`, because `remap --check` errors on an empty
  or absent `.host-remap`, so a no-rename case-(a) adoption cannot pass a `done`
  recheck.
- Push auth to `connollydavid/agentic-UDPspeeder-simd` is intermittent: the stored
  credential is the `slartibardfast` token, which 403s after the first few pushes
  landed. If `git push` 403s, surface it to the operator rather than retrying or
  swapping credentials. As of this entry, `f8d36ed` and `5ec59af` are local only.

## 2026-07-03 — followed the host procedure: conformant, no upgrade available

- Ran the case-(c) upgrade/verify cycle from the `host` procedure
  (`github.com/connollydavid/host`). `host-template` upstream is still at `565410a`,
  the exact revision the `.host` stamp adopted: a `git fetch` in the submodule found
  no commits after it, and `565410a` is an ancestor of `origin/main`.
  `host-lifecycle upgrade .` reports up to date (baseline `46a1fd2`, 0 out of order).
  With no newer methodology to pull in, following the host reduced to the verify gate.
- Verify gate is green. `host-lifecycle software --check .` exits 0 (both components at
  pin, every phase receipt valid, reconcile clean, prose clean, no worktree-symlink
  hazards); `validate plan/` and `validate call/` both `ok`; `host-lint --all` and
  `--log` clean. Independently confirmed: udpspeeder-simd worktree is at pin `3374e3b`
  on `branch_libev` with a clean tree, host-lint at `78804cd`, and the commit-msg hook
  still rejects an ordinal tell (a `phase 1` message exits 1, a clean message exits 0).
- udpspeeder-simd still carries no `.allium`/`.tla` spec, so the requirements and timing
  lanes stay inert and there is no spec-without-lane defect. Every spec found on disk
  belongs to a tool's own worktree, not to the software under development.
- Standalone `host-lint --prose` on the authored docs prints advisory `note:` lines but
  exits 0. Those notes are below the enforced bar; the in-process prose audit inside
  `software --check` is the gate that binds and it reports no flagging or warning tropes.
  Most notes sit in verbatim copied-in content (the `UPGRADING.md` ledger,
  `cast/applying-personas.md`) that is not reworded locally. The notes are not a red gate.
- Corrects the 2026-07-03 "push auth is flaky" entry above: the commits it listed as
  local-only (`f8d36ed`, `5ec59af`) are now pushed. `HEAD == origin/main` and the tree
  is clean. Push auth may still 403 intermittently; surface it to the operator if it does.

## 2026-07-03 — embedded the packages feed as a second software lane

- Added `packages` (a fork of `openwrt/packages`, GPL-2.0, an OpenWrt feed of
  Makefiles/shell/C) as a Where-room component in `.host-software`: source pin
  `1d40ad9` on canonical branch `master`, no build/artifact (migrated build-recipe
  feed, not a built artifact). Materialized to `software/packages/master/`;
  `software --check` is green.
- Mechanics for a new component: host-lifecycle has no `software --add`, so a new
  lane is a hand-edited `.host-software` stanza plus `software --materialize --item
  <name> .` (the `--item` scope avoids re-touching existing worktrees). The embed and
  release phase receipts are written with `host-lifecycle receipt --record <phase>
  --component packages --disposition done|skip (--evidence|--reason) .`; a new
  component HAZARDs on missing embed+release receipts until both are recorded.
- Key rule (call/0003): commits in the packages worktree carry NO `Co-Authored-By:
  Claude` trailer, so the feed stays upstream-clean for `openwrt/packages`. The
  operator confirmed the scope is packages only, so host-repo commits keep the
  trailer. Recorded in call/0003 and the CLAUDE.md packages project-specifics.

## 2026-07-03 — push-auth root cause: slartibardfast is pull-only; helper is `store`

- The recurring push 403 has a concrete root cause rather than flakiness.
  `gh api repos/connollydavid/agentic-UDPspeeder-simd` shows the `slartibardfast`
  account has `push: false` (pull only); the owner account `connollydavid` (also
  logged in to gh) has push. And git's credential helper here is `store`
  (`~/.git-credentials`), not gh, so `gh auth switch -u <user>` does not change the
  token `git push` sends. The store already holds slartibardfast's token, so pushes
  go out as slartibardfast and are denied.
- To push as slartibardfast (the operator's intended identity), grant slartibardfast
  write on the repo; then a plain `git push` works with no helper change. To make
  `gh auth switch` actually route pushes, run `gh auth setup-git` so git uses the
  active gh account's token. Do not push as connollydavid without operator direction:
  it changes the public push identity, and the operator is provenance-sensitive.
- Pending operator decision (asked, away from keyboard): grant slartibardfast write,
  push as connollydavid, or operator pushes manually. As of this entry `main` is ahead
  by 7 unpushed commits (packages embed, call/0003, CLAUDE.md, two memory entries, the
  earlier verify-sweep entry, and the three-persona commit).

## 2026-07-03 — resolved: push as connollydavid via a one-shot gh credential

- Operator chose to push as the owner. The working recipe: `gh auth switch -u
  connollydavid`, then
  `git -c credential.helper= -c credential.helper='!gh auth git-credential' push origin main`.
  The empty `credential.helper=` resets the inherited `store` helper (which holds
  slartibardfast's read-only token and 403s), and the gh helper then supplies
  connollydavid's token for that one push, with no change to global git config.
- All pending commits landed (`23bdc1f..6f1e66a`); `main` is in sync with origin.
- Going forward: repeat that one-shot override, or run `gh auth setup-git` once (with
  connollydavid active) and clear the stale store token so a plain `git push` works.
  slartibardfast stays read-only on the repo (not a collaborator); grant it write only
  if a bot-identity push is wanted later. This supersedes the earlier "push auth is
  flaky" framing: the cause was permissions plus a static store token, not flakiness.

## 2026-07-03 — published the book to GitHub Pages

- Ran the publish phase. `host-lifecycle book .` (v0.35.1) writes book.toml with
  `src = mdBook/src` and `build-dir = mdBook/out`, a SUMMARY in lifecycle order, and 17
  pages; `book --check .` passes (every room renders: cast 5, plan 1, software 1, call 4,
  reference 4, memory 1). book.toml and mdBook/ are gitignored generated output.
- Fixed two defects in the reference doc-site workflow. It was named `site.yml`, but the
  publish-phase recheck is `test -f .github/workflows/mdbook.yml`, so a `done` publish
  receipt would HAZARD until the file is named `mdbook.yml`. It also published `./book`,
  while v0.35.1 builds to `mdBook/out`. Renamed to mdbook.yml, set
  `publish_dir: ./mdBook/out`, and corrected the stale `src=docs` comment. Both look like
  template bugs at revision 565410a, worth proposing upstream.
- CI (`mdbook.yml`, on push to main) builds with mdbook v0.4.40 and deploys mdBook/out to
  the `gh-pages` branch via peaceiris/actions-gh-pages. GitHub Pages was disabled (the
  `/pages` API returned 404), so enabled it from gh-pages root with
  `gh api -X POST repos/connollydavid/agentic-UDPspeeder-simd/pages -f source[branch]=gh-pages -f source[path]=/`.
  The site is live at https://connollydavid.github.io/agentic-UDPspeeder-simd/ (HTTP 200).
- Publish receipt flipped from skip to done; `software --check` is green (the recheck now
  finds mdbook.yml). Verified locally with the pinned mdbook v0.4.40 before pushing.

## 2026-07-03 — udpspeeder-simd package builds clean against the x86_64 SDK

- SDK approach pivoted. `make world` was excessive; used the public prebuilt x86_64
  snapshot SDK (openwrt-sdk-x86-64_gcc-14.4.0_musl, the one OpenWrt CI uses) rather than a
  from-source build. The embedded `openwrt` component stays but is not needed for this path
  and adds ~2.5 min to `software --check` (flagged for the operator to keep or remove).
- OpenWrt needs a case-sensitive FS: /mnt/c is case-insensitive and the build refuses it,
  so software/openwrt is symlinked to ext4 (/home/dconnolly/host-stores); the SDK and its
  build_dir also live on ext4.
- The package (net/udpspeeder-simd, authored in the packages worktree) built cleanly:
  `make package/udpspeeder-simd/compile` produced udpspeeder-simd-2026.07.03~3374e3bb-r1.apk
  (snapshot uses .apk, not .ipk). No fork change was needed — the udpspeeder-style cc_cross
  + gitversion Build/Prepare sufficed, and the makefile's `export STAGING_DIR=/tmp/` did not
  break it. Dynamic linking confirmed by deps libc/libstdcpp6/librt/libatomic1.
  PKG_MIRROR_HASH = 225c0fef087e56c190ec1a626fc244a0e32f1f791d5e22efe604e962026c4698.
- Task receipts done: #fork-build, #feed-package, #service-integration. Pending: #test-script
  (CI runs it), #ci-sdk-lane, #interop, #pr, #backports. The package files are authored in the
  packages worktree but NOT yet committed or pushed to the fork; the branch strategy and the
  outward push/PR await operator go.

## 2026-07-03 — udpspeeder-simd pushed to the fork on a feature branch (PR held)

- Operator chose fork + PR, but the PR needs a review round, so it is NOT opened. Committed
  net/udpspeeder-simd/ (Makefile + files + test.sh) on branch `udpspeeder-simd` of
  connollydavid/packages, commit db858a8, pushed. Author + DCO Signed-off-by = David Connolly
  <david@connol.ly> (real name + public email, no Claude trailer, per call/0003 + OpenWrt rules).
  Subject "udpspeeder-simd: add package"; body references
  https://github.com/openwrt/packages/issues/28562.
- The packages worktree had no git identity; set it to David Connolly / david@connol.ly. The
  canonical master worktree was used in-place to make the branch then restored to master @
  1d40ad9, so the .host-software pin and software --check stay intact; the feature branch lives
  on the fork, not as a host-tracked worktree.
- Open the PR (after review) from
  https://github.com/openwrt/packages/compare/master...connollydavid:packages:udpspeeder-simd?expand=1
  Before submitting, consider syncing the fork onto current openwrt/packages master (the branch
  is based on the fork's master 1d40ad9, which may be behind upstream).
- openwrt embed KEPT (operator decision), despite the ~2.5 min software --check cost.
- Receipts: #fork-build/#feed-package/#service-integration/#interop done; #pr held (review round);
  #test-script + #ci-sdk-lane pending (CI); #backports policy-constrained.
- Update: rebased the branch onto current upstream openwrt/packages master (333bf60); tip is now
  a7f0f087, a single commit with no merge commits in the PR range; force-pushed to the fork.
  Formalities self-check (against .github/formalities.json) passes: crlf=0, subject 28<=60,
  body<=79, DCO Signed-off-by matches a non-noreply author, conffiles declared, openwrt-meta
  present, no patches. Open review-round items: Run Testing details (built x86_64 via the
  snapshot SDK gcc-14.4.0 + CI test.sh; a physical-device run is optional but stronger), and a
  release-notes line if the formalities bot requests one.

## 2026-07-03 — PR opened to openwrt/packages (pull/29901)

- Opened https://github.com/openwrt/packages/pull/29901 ("udpspeeder-simd: add package") as
  connollydavid, from connollydavid:udpspeeder-simd to openwrt:master, referencing the issue.
  Confirmed host-side clean first: main == origin, fork branch a7f0f087 synced, four receipts
  done. Release notes are in the PR body (a section), testing framed as x86_64 build + CI
  test.sh (operator accepted that trade-off).
- Corrected the plan: #pr no longer depends on #ci-sdk-lane. The operator directed opening the
  PR against OpenWrt's own CI, so the fork-side SDK CI lane is independent, not a prerequisite.
  Recorded #test-script done (script added + wired; the PR CI exercises it) and #pr done.
  Pending: #ci-sdk-lane (fork-side, optional) and #backports (policy: new packages are not
  normally backported to release branches).
- Next: watch the PR's FormalityCheck + multi-arch build. If the bot wants release notes in a
  different form, amend and force-push the fork branch.

## 2026-07-03 — addressed the Copilot review; fork version-banner fix; idiomatic test.sh

- Copilot flagged two on PR 29901, both valid: test.sh could false-positive (its grep matched
  the program name, which a dynamic-loader error echoes), and the init had `fix_latency`
  non-local plus a duplicated `sock_buf`. Both init issues were inherited verbatim from
  net/udpspeeder (the sibling has the same bugs). @codemarauder is Nishant Sharma, the
  net/udpspeeder maintainer; offered him co/primary maintainership of udpspeeder-simd in the
  PR comment.
- Idiomatic gap and its fix: OpenWrt test.sh idiomatically greps the package version, but the
  binary's print_help() truncated gitversion to 10 chars (`strncpy(...,10)`), so a full-version
  grep would miss. Fixed the fork (main.cpp copies the full string; commit 2e12e5b pushed to
  branch_libev), re-pinned .host-software to 2e12e5b, updated the package (PKG_SOURCE_VERSION
  2e12e5b, PKG_MIRROR_HASH 6d4564dc, PKG_VERSION now 2026.07.03~2e12e5b4), and switched test.sh
  to `grep -qF "$PKG_VERSION"`. Amended the single PR commit (7f5bc7c8), force-pushed; PR still
  discrete (4 files). Posted a terse reply comment (#issuecomment-4877656043).
- Rebuilt via the SDK (exit 0) for the new hash. The runtime version-grep is confirmed by
  OpenWrt's PR CI, since the cross-built musl binary cannot run on this host.
- Scope decision: we will NOT touch net/udpspeeder (operator). Removed the "happy to send a
  separate PR" offer from the PR comment (edited #issuecomment-4877656043); the sibling's same
  two init bugs are left alone.

## 2026-07-03 — OpenWrt PR #29901: 32-bit ARM build fix in the fork

- The PR's multi-arch CI (openwrt shared `Feeds Package Test Build`) ran and failed
  only on `arm_cortex-a15_neon-vfpv4` and `arm_cortex-a9_vfpv3-d16`; aarch64, mips_24kc,
  x86_64, i386, powerpc, riscv64 all passed. Root cause was in the fork source, not the
  package: `xor_spe.S` marked the stack non-exec with `.section .note.GNU-stack,"",@progbits`.
  On 32-bit ARM `@` starts a line comment, so gas ate `@progbits` and reported "junk at
  end of line, first unrecognized character is `,`". aarch64/mips/ppc/riscv/x86 do not use
  `@` as a comment char, which is why only 32-bit ARM broke.
- Fix (universal, per call/0005 — build adjustments live in the fork): spell it
  `%progbits`. gas accepts `%` for the ELF section type on every target (verified locally:
  x86 g++ assembles both `@progbits` and `%progbits`), and `%` is the required form where
  `@` is a comment. Fork commit `c2b3759` on `branch_libev`.
- Propagation: re-pinned `.host-software` udpspeeder-simd → c2b3759; bumped the PR's
  `net/udpspeeder-simd/Makefile` PKG_SOURCE_VERSION → c2b37590 and refreshed
  PKG_MIRROR_HASH → d6f564823fa0217788bc937e06c71266bfa3a457d0803912b2d10bcb9957d3ba
  (amended the single PR commit, force-pushed; PR head 5d8ed050). Kept the fork commit's
  Claude co-author trailer; the packages commit has none (call/0003).
- Mirror-hash regen recipe (local x86_64 SDK): set PKG_MIRROR_HASH to 64 zeros, run
  `make package/<pkg>/download V=s`; the download clones, packs the reproducible git
  tarball, and prints `got <real-hash>`. `skip` does NOT work for a git-proto source
  (the github archive downloader refuses without a real sha256). Then compile to confirm.

## 2026-07-17 — OpenWrt PR #30015 (net/udpspeeder) + timeout fold into PR #29901

- Opened https://github.com/openwrt/packages/pull/30015 (net/udpspeeder) against
  openwrt/packages:master from connollydavid/packages:udpspeeder-toolchain-flags. Two atomic
  commits, PKG_RELEASE 3→4→5:
  - `udpspeeder: build with the toolchain CXX and flags`: new patch
    010-build-with-toolchain-flags.patch builds the cross target with $(CXX) and honours
    $(CXXFLAGS)/$(LDFLAGS), makes gitversion overridable; package drops the Build/Prepare sed
    hacks, injects the version via MAKE_FLAGS, adds PKG_BUILD_FLAGS:=no-mips16.
  - `udpspeeder: pass the timeout option to the binary`: adds
    `procd_append_param command --timeout "${timeout}"` after --mtu in files/udpspeeder-init.
    `Fixes: .../issues/18955` auto-closes on merge. The option was validated and shipped in the
    sample config (tunnel2) but never passed to the binary.
- no-mips16 is REQUIRED, not cosmetic: honouring CXXFLAGS pulls -mips16 onto
  mips_24kc/mipsel_24kc, where C++ std::atomic emits a `sync` barrier MIPS16 cannot encode
  ("opcode not supported on this processor: mips2 (mips2) 'sync'"); no-mips16 strips it (MIPS32).
- Non-drift confirmed from binary help: `--timeout ... unit: ms, default: 8ms`; UCI schema
  default is 8, so wiring it is a no-op at the default and just makes the advertised option work.
- Verified locally via snapshot SDK on all ten CI arches (scratchpad/build_all.sh): all pass;
  both mips controls (without no-mips16) fail on the sync opcode, proving necessity.
- PR #29901 (net/udpspeeder-simd) had the identical latent timeout bug. Folded the same
  `--timeout` line into the single `udpspeeder-simd: add package` commit (amend, NO PKG_RELEASE
  bump since 1.0.0-1 is unreleased); force-pushed connollydavid:udpspeeder-simd → 3540c71ce.
  Posted a terse alignment comment (#issuecomment-5002468098) referencing #30015.
- Hygiene: packages commits carry NO Claude trailer (call/0003); sign-off = author = David
  Connolly <david@connol.ly>. #30015 rebased onto current upstream/master (net/udpspeeder
  untouched upstream); #29901 left on its older base (PR diff is clean vs merge-base and CI
  builds on the snapshot SDK, so no rebase needed and none requested). .host-software NOT
  re-pinned (feature-branch work; the master pin is unchanged).

## 2026-07-17: #30015 "Dirty patches detected" — patches must be quilt-refreshed

- All ten Feeds Package Test Build jobs failed at `make package/udpspeeder/refresh`: the CI
  requires each patch byte-identical to quilt's canonical output. Our patch applied at exact
  offsets with no fuzz, yet still failed.
- Root cause: OpenWrt refreshes with `QUILT_DIFF_OPTS="-p" quilt --quiltrc=- refresh -p ab
  --no-index --no-timestamps` (openwrt/openwrt include/quilt.mk), and GNU diff `-p` appends
  function context to hunk headers (`@@ -51,7 +51,7 @@ cygwin:git_version`). `git format-patch`
  output lacks the suffix, so the refresh rewrites the file and the git-diff check trips.
- Fix recipe: extract the pinned source (`git archive 20230206.0`), set up `patches/` + series,
  `quilt --quiltrc=- push -a`, run the refresh command above, copy the refreshed patch back.
  Verified idempotent: a second refresh reports "is unchanged". Quilt preserves the git header
  (From/Subject/Signed-off-by/diffstat) untouched.
- Folded into the toolchain commit via `commit --fixup` + `GIT_SEQUENCE_EDITOR=: git rebase -i
  --autosquash`; range-diff showed only the two hunk-header lines changed, timeout commit
  byte-identical (`=`). Force-pushed `7a76af810...075f4a7e0` (lease + force-if-includes).
- Lesson: any patch destined for openwrt/packages should be generated or round-tripped through
  quilt with those exact args before committing, not taken raw from git format-patch.

## 2026-07-31 — upstream merged our toolchain-flags PR; taking it in both packages

- wangyu-/UDPspeeder merged https://github.com/wangyu-/UDPspeeder/pull/356 (686d6079), then
  reshaped it in b6a1b594: `cross` was restored to the hardcoded `${cc_cross}`, and the change
  landed as a NEW target instead:
  `cross_cxx: ${CXX} -o ${NAME}_cross -I. ${SOURCES} ${FLAGS} -O2 ${CXXFLAGS} ${LDFLAGS} ${LDLIBS}`.
  Three deltas vs what we sent: `-O2` moved BEFORE `${CXXFLAGS}` (so a caller's -Os wins instead
  of being overridden), `-lrt` dropped, `${LDLIBS}` added. Our `gitversion ?=` hunk survived
  verbatim, so MAKE_FLAGS version injection still works.
- Consequence for the merged net/udpspeeder patch: its second hunk (the `gitversion ?=` line) can
  no longer apply to any source at or past b6a1b594, since upstream already has it. So the patch
  had to be dropped as part of a version bump, not deferred.
- `-lrt` is a no-op on OpenWrt, PROVEN not assumed: musl's `librt.a` in the toolchain is an 8-byte
  empty archive (clock_gettime is in libc), and the packaged binary built with `LDLIBS="-lrt"` and
  without it are byte-identical (sha256 502163f5...). NEEDED is libstdc++/libgcc_s/libc either way.
  So neither package passes -lrt; a toolchain that needs it can pass LDLIBS. Left `DEPENDS:=+librt`
  alone in both (inert: musl's libc provides it) rather than widen the diff.
- The 3-year source bump 20230206.0 -> b6a1b594 is WIRE-SAFE, also proven: the only functional
  change is swapping the in-tree `crc32h` for Stephan Brumme's `crc32_fast`. Both are standard
  zlib CRC-32 (poly 0xEDB88320, init ~0, final complement); a comparison harness over every length
  0..2048 x 8 random buffers matched exactly, and both give 0xCBF43926 for "123456789". The rest is
  typo fixes, an `is_vaild`->`is_valid` rename, and a djb2/sdbm loop rewrite that removes a
  one-byte over-read without changing the hash.
- OpenWrt version convention for an untagged git source is `<base>~<shortsha>` + a full-sha
  PKG_SOURCE_VERSION. Careful: `~` sorts BEFORE end-of-string (Debian style), so `20230206.0~<sha>`
  would sort BELOW the released 20230206.0 and break the upgrade path. Used `20260731~b6a1b594`
  (commit date as base) so it sorts above.
- Fork: added the same `cross_cxx` target (commit 81fde6c, tagged v1.0.1, pushed); kept our
  cross/cross2/cross3 as-is since this fork deliberately dropped the hardcoded compiler paths.
  Re-pinned .host-software to 81fde6c.

## 2026-07-31 — correction: PR #29901 has no test.sh (the 2026-07-03 entry is wrong)

- The 2026-07-03 entry above says "#test-script done ... test.sh added beside the Makefile;
  exercised by the OpenWrt PR CI runtime test", and `.host-task-receipts` records the same
  evidence for `plan/0000#test-script`. Both are FALSE as of now, and have been since 2026-07-04.
- Traced through the branch reflog: test.sh survived to b7ef6490 (2026-07-04 21:31) and was gone
  in the very next amend, b9e331ec (2026-07-04 23:16), the one that fixed the Build/Prepare
  double-expansion. It was dropped accidentally, not by decision, and every later force-push
  carried the loss forward. The PR head has carried three files (Makefile, config, init) ever
  since, so the CI arches flagged `runtime_test: true` have had nothing to run.
- Operator decision on 2026-07-31: LEAVE IT OUT rather than restore it, so the package ships
  without a runtime test. BKPepe had questioned the script anyway ("Do we need this script at
  all? This should be covered by generic testing"). The `#test-script` receipt is therefore
  stale and should be re-dispositioned by the operator (it is a tool-written ledger; not
  hand-edited here).
- Lesson: an amend that fixes one file can silently drop another. Diff the file LIST against the
  PR head after every amend + force-push, not just the file contents.

## 2026-07-31 — OpenWrt packaging idioms, and how to test under qemu properly

- VERSION FORM for an untagged git source: do NOT hand-write PKG_VERSION. Set PKG_SOURCE_DATE
  plus a full-sha PKG_SOURCE_VERSION and let include/download.mk derive it:
  `PKG_VERSION := $(subst -,.,$(PKG_SOURCE_DATE))~$(call version_abbrev,$(PKG_SOURCE_VERSION))`,
  giving `2026.07.31~b6a1b594` (version_abbrev = 8 chars; it returns the FULL sha under DUMP, so
  the feed index shows the long form while the build uses the short one). Feed usage: 96 packages
  use PKG_SOURCE_DATE vs 3 that hand-write a `~` version. Changing the version form changes
  PKG_MIRROR_HASH, since the tarball's inner subdir is $(PKG_NAME)-$(PKG_VERSION).
- UPSTREAM UDPspeeder TRUNCATES THE VERSION: print_help does `strncpy(buf, gitversion, 10)`, so
  `--help` (the flag OpenWrt's generic check finds) shows ten characters only. The old version
  `20230206.0` was ten characters exactly, so the check passed by luck for years. Any longer
  version needs `test-version.sh`, the idiomatic override (70 in the feed). Our simd fork already
  prints the full version, so only net/udpspeeder needs the override.
- DEPS ARE DERIVED FROM THE ELF: include/package-pack.mk runs scripts/gen-dependencies.sh, which
  reads NEEDED and FAILS the build for a linked library that is not declared. It never checks for
  extras, so a declared-but-unlinked dep is inert. librt and libatomic were both provably inert:
  70/70 builds and packet tests across all 35 published architectures with both removed, no binary
  NEEDs either, and no `__atomic_*`/`__sync_*` symbol anywhere. On musl, Package/librt/install
  copies nothing at all (`ifneq ($(CONFIG_USE_MUSL),y)`).
- RUNTIME TESTS, the idiom: `test.sh <pkgname> <version>` runs INSIDE a target-arch container
  (binfmt + qemu-user-static) with the package installed. `pre-test.sh` installs test deps
  (`apk add socat`). A package-specific test.sh REPLACES the generic tests (version check
  included), and test-version.sh is only consulted by the generic path, so test.sh must assert the
  version itself. BusyBox in OpenWrt is built with NC_SERVER=n and NC_EXTRA=n, so nc can neither
  listen nor exec: use socat via pre-test.sh. Do not use a fixed sleep, the container is emulated;
  retry the payload instead.
- QEMU CPU MODELS, do not trust the default. powerpc_8548 (CPU_TYPE 8548, e500v2) fails under the
  default 32-bit PPC model with an illegal instruction, and it is NOT the package: the faulting
  word disassembles to `iseleq` inside musl libc, which holds 63 isel instructions while our
  binaries hold none. `-cpu e500v2_v10` runs it. Control: the musl loader alone faults under the
  default and prints its version under e500v2_v10. Every arch now names a verified model in
  .github/scripts/arch-map.tsv; where qemu-user lacks the exact CPU the closest SUPERSET is used
  (xscale and fa526 -> arm926, cortex-a5 -> cortex-a7, pentium-mmx -> pentium2, pentium4 -> n270,
  since a weaker model invents failures and a richer one hides them and skews feature detection).
- PROBE BY OUTPUT, NOT EXIT STATUS: musl's loader prints its version and exits 1. A first pass at
  CPU discovery keyed on exit status and reported every architecture broken. Judge the output.
- SCOPE: OpenWrt's CI runtime-tests only aarch64_generic, arm_cortex-a15_neon-vfpv4,
  i386_pentium-mmx, mips_24kc and x86_64; powerpc_8548 is runtime_test:false. So the CPU-model
  work is OUR local lane's concern, not something the OpenWrt PR depends on.
- arm_fa526 (gemini) is BUILD-ONLY under qemu-user, and the cause is the emulator, not the
  package. That target compiles plain ARMv4: its binary holds ZERO bx/blx, where the ARMv5 build
  of the same package holds 133, so it cannot enter Thumb code at all. qemu-user always maps a
  Thumb vdso, so the call to __vdso_gettimeofday runs Thumb bytes in ARM state and branches to a
  wild address; the in_asm trace ends in `IN: __vdso_gettimeofday` decoding 46c046c0 (Thumb
  nop;nop) as ARM and branching to 0x40b2838c, exactly the SIGSEGV si_addr. Proven not ours two
  ways: the CURRENTLY SHIPPED 20230206.0 package fails identically under -cpu arm926, and a
  trivial C++ program against the same musl and libstdc++ runs fine there. Real hardware never
  meets it, since the Linux ARM vdso needs ARMv7 and a gemini kernel supplies none, leaving musl
  on plain syscalls. qemu-user has no flag to withhold the vdso, so the packet test is skipped
  for that arch rather than run under a v7 model that would hide real mismatches.

## 2026-07-31 — udpspeeder-simd crashed on x86_64 without SSSE3 (found by faithful qemu models)

- lib/fec.cpp initialised `addmul1_x86_fn = addmul1_ssse3` and only ever RAISED it to AVX2 or
  AVX-512. Nothing probed SSSE3, and x86_64 does NOT imply it: AMD K8/K10 (Athlon 64, Opteron,
  Phenom, Phenom II, Athlon II) lack it, as do early 64-bit Intel parts; AMD added it with
  Bulldozer in 2011. Those CPUs took SIGILL on the first PSHUFB in the Reed-Solomon inner loop,
  so the tunnel died on its first FEC batch. Upstream udpspeeder was unaffected.
- Only visible under a faithful CPU model. Every earlier sweep used qemu's DEFAULT x86_64 model
  (rich), and OpenWrt's own CI runtime-tests x86_64 on a GitHub runner that has SSSE3/AVX2, so the
  bad path never ran. It appeared the moment the map named `-cpu qemu64` (the AMD64 baseline).
- Fix (fork v1.0.2, f3834047): pointer starts at scalar and rises only as CPUID allows, via
  cpu_has_ssse3() (leaf 1 ECX bit 9) and cpu_has_sse2(); new SSE2 addmul1 sits beneath SSSE3, so a
  CPU without PSHUFB still vectorises. SSE2 has no byte shuffle, so it multiplies by repeated
  doubling: `_mm_add_epi8(x,x)` for the shift and `_mm_cmpgt_epi8(0,x)` to select the reduction.
  The reduction constant is read from `gf_mul_table[2][0x80]`, not hardcoded, so it follows the
  field. Measured 1.73x scalar at 1500B (913 vs 1579 ns); ssse3 is 9.8x.
- Also hardened packet_cook.cpp: its AVX2 tier was set from CPUID leaf 7 EBX bit 5 ALONE, with no
  OSXSAVE/XCR0 check and no max-leaf check. Now mirrors the correct probe.
- Test method worth reusing: `bench_addmul1_force(name)` pins one implementation so test_fec can
  hold EVERY path against scalar over all 256 multipliers and sizes hitting each loop and tail.
  Ran the suite under `qemu-x86_64 -cpu qemu64|Nehalem|Haswell` to exercise sse2/ssse3/avx2.
  AVX-512BW cannot be verified this way: qemu-user leaves ZMM state disabled in XCR0, so the
  OS-support check correctly declines it.
- HARNESS BUG worth remembering: `find ... | head -1` picked a STALE build dir from an earlier
  session in a reused SDK, so one x86_64 result described a binary nobody had built that run.
  Select by newest mtime (`-printf '%T@ %p'| sort -rn`). Fresh CI SDKs never hit this; local
  reused SDKs do.

## 2026-07-31 — qemu64 is not the x86_64 floor; the first Opteron is

Asked whether we are aligned with the very first x86_64 chip, and the honest answer needed
evidence at both ends rather than an assertion. Findings worth keeping:

- `-cpu qemu64` GRANTS SSE3. It caught the SSSE3 crash, but it is not the architectural floor and
  never was. The floor is `-cpu Opteron_G1,-sse3`: qemu's model of the AMD Opteron 240 of 2003,
  the first x86_64 silicon, with SSE3 subtracted for the earliest stepping. SSE3 only arrived on
  K8 revision E in 2005. The arch map's x86_64 row now names that model.
- Compile-time floor is already right: the OpenWrt x86_64 toolchain defaults to `-march=x86-64`
  with sse3, ssse3, sse4, cx16 and popcnt all DISABLED (`gcc -Q --help=target` proves it, and
  `CONFIG_TARGET_OPTIMIZATION` is only `-Os -pipe`, so nothing raises it).
- `XGETBV` IS NOT BASELINE. It arrived with XSAVE in 2008, so a K8 faults on it. Our probes check
  CPUID leaf 1 ECX bit 27 (OSXSAVE) first, and the EMITTED code keeps the order: every xgetbv sits
  behind `bt $0x1b,%ecx` / `jae`. Verified in the disassembly, not just the source. Worth
  re-checking after any compiler bump, since the guard is a branch the optimiser could in
  principle move.
- CRC32C's hardware path is behind `crc32c_has_hw()` (leaf 1 ECX bit 20, SSE4.2) and falls back to
  the slicing-by-8 table, so it is safe on K8 too.
- Static screen worth reusing, the x86 analogue of isa-check.sh: disassemble and list every
  mnemonic outside the baseline together with its containing function. `udpspeeder` holds ZERO;
  `udpspeeder-simd` confines all of them to `addmul1_{ssse3,avx2,avx512}`, `xor_tile_{avx2,avx512}`
  and `crc32c_hw`, each reached only through CPUID. That is the property to hold, not "it ran".
- Dynamic proof: both packages pass the packet test under `Opteron_G1` and `Opteron_G1,-sse3`, and
  test_udpspeeder under those models selects sse2 and agrees with scalar over all 256 multipliers,
  declining ssse3/avx2/avx512bw.
- Reading tests through a grep can invent a hollow section: filtering on "addmul1" hid the tier
  results, whose pass lines read "sse2 agrees with scalar". Read the section, not a keyword.

## 2026-07-31 — the x86 lacuna: OpenWrt has three x86 package arches, not one

Asked whether x86 coverage is complete. It was not, and the gap was in the emulation models
rather than in the architecture list.

- OpenWrt publishes FOUR x86 subtargets (64, generic, geode, legacy) but THREE package
  architectures. geode and legacy declare no CPU_TYPE, so both fall to the i386 default of
  `pentium-mmx` (include/target.mk). One row covers the pair; generic is pentium4; 64 is x86_64.
- BOTH i386 models were too rich, the same failure as qemu64 on x86_64:
  - `n270` (Atom) HAS SSSE3, so the i386_pentium4 job selected the SSSE3 path and never once ran
    the SSE2 tier a real Pentium 4 uses. Now `pentium3,+sse2`, which is exactly a P4's ISA.
  - `pentium2` HAS CMOV, which a Geode GX/LX and a Pentium MMX do not. Now `pentium,+mmx`.
- qemu-user genuinely gates these, proven by one-instruction controls rather than assumed:
  `pentium2` runs cmov and faults on pshufb; `pentium2,-cmov` and `pentium,+mmx` fault on cmov;
  `n270` runs BOTH cmov and pshufb; `pentium3,+sse2` runs movdqa and faults on movddup. Feature
  subtraction/addition on a stock model works, so compose the model instead of borrowing one.
- Static screen of the geode build: nothing above the floor outside CPUID-guarded functions. The
  one CMOV lives inside `addmul1_ssse3`, which GCC is free to emit because `target("ssse3")`
  implies P6, and it only ever runs on a CPU that has SSSE3 and therefore CMOV. Not a defect.
- All three x86 arches pass both packages under the tightened models.
- `mips_4kec` and `riscv64_riscv64` DO have package directories on the buildbot, so the listing
  alone suggests 37 arches. They are frozen: last built April and July of 2025 against zlib 1.3.1,
  where a live arch carries a build from this month. Check the DATES, not the directory.

## 2026-07-31 — MMX helps the XOR and hurts the multiply; measure per path

"MMX is still SIMD" — and OpenWrt's lowest x86 arch (i386_pentium-mmx, from geode and legacy) has
MMX and nothing above it. So the fork was taken down to that floor. Two opposite results, and the
lesson is that "add a lower SIMD tier" is not one decision but one per kernel.

- MMX addmul1: WRITTEN, MEASURED, REVERTED. The repeated-doubling multiply costs ~5 ops/byte at
  MMX's 8-byte width, against ONE L1-resident load per byte for scalar, which indexes a single
  256-byte row of gf_mul_table for a fixed c. Measured on a real 32-bit build: mmx 0.55x scalar
  (3166 vs 1738 ns at 1500B); sse2 1.70x. SSE2 only wins by doubling the width. The floor keeps
  the scalar table, which is correct AND faster.
- MMX xor_tile: KEPT. XOR is one op per width, so width converts straight into throughput.
  Against the four-byte word path i386 actually had: mmx 1.46x, sse2 3.08x.
- The bigger find: packet_cook.cpp's ENTIRE x86 SIMD block was `#if defined(__x86_64__)`, so every
  32-bit build used the 4-byte word loop — including i386_pentium4, which has SSE2. x86/generic is
  a commonly used target, so that was a 3.08x left on the floor for years. fec.cpp had already been
  widened to __i386__; packet_cook.cpp had not. When widening one file's ISA guards, grep for the
  same guard elsewhere.
- MEASURE 32-BIT MMX ON A 32-BIT BUILD. On x86_64 GCC emulates __m64 with SSE (TARGET_MMX_WITH_SSE),
  so an x86_64 measurement of MMX is not MMX. Build with the OpenWrt i386 toolchain and run the
  binary natively (WSL2 runs i386 ELF fine); qemu timings are useless for ISA ratios.
- EMMS is mandatory: MMX registers alias the x87 stack and the tunnel does FP work in its timers.
- Renaming a force() tier label silently turns the reference call into a no-op, so the test compares
  a tier against itself and always passes. Renamed tier 0 "scalar"->"word" and had to fix the test's
  reference call in the same breath. A hollow green, exactly the shape call/0035 warns about.

## Dispatch is a separate claim from implementation, and it needed its own lane

The tier comparisons pin a path and hold it against a reference. That says nothing about which path
the dispatcher CHOOSES, and the choice is what the SSSE3 fault broke. A CI runner carries every
feature, so it always chooses the top path; no runner-only job can see the bug class.

- Three runtime dispatchers exist, not one: addmul1 (fec.cpp), xor_tile (packet_cook.cpp) and crc32c
  (crc32c.h, an SSE4.2 probe resolving a function pointer on first call). All three now report their
  choice through bench_*_auto() and are held to EXPECT_ADDMUL1 / EXPECT_XOR_TILE / EXPECT_CRC32C.
- The auto hook must RE-DERIVE, not read back. bench_addmul1_force() overwrites the pointer, so the
  reporter re-runs the real selection (addmul1_select(), extracted from init_fec) and the selection
  now resets to scalar first rather than only raising. Reading the pointer back would report whatever
  a previous test pinned.
- QEMU TCG IMPLEMENTS NO AVX-512 AT ANY CPU MODEL (checked on qemu 11.0.2): -cpu Skylake-Server warns
  "TCG doesn't support requested feature ... avx512bw", clears the CPUID bit and leaves XCR0 at 0x207
  rather than 0xE6. So the AVX-512 path cannot be exercised under emulation at all, on any model,
  ever. That row instead proves the gate DECLINES on a part whose model name says otherwise. AVX-512BW
  correctness is verified only when a GitHub runner happens to land on an Intel host.
- The OpenWrt i386 toolchains default to -march=i486, so the march must be named explicitly to
  reproduce what OpenWrt ships (pentium-mmx for geode/legacy, pentium4 for generic).
- A pentium-mmx-built binary runs clean on qemu's 486 model and correctly selects scalar/word/sw, so
  the bottom rung of the ladder is reachable and tested even below OpenWrt's own floor.
- The Makefile forces `export STAGING_DIR=/tmp/`, which overrides the environment, so the OpenWrt
  toolchain wrapper only warns and no STAGING_DIR needs setting for a `make test-cross` build. It
  matters only when invoking the cross gcc directly.

## The SPE XOR was never shipped, and the package could not have told us

The e500v2 SPE unit does the tile XOR 64 bits at a time. That path needs `SPE=1` on the make line,
and `net/udpspeeder-simd` passes only `cross_cxx gitversion=...`, so **every mpc85xx build ever
shipped has used the word path**. Confirmed by objdump: with the flag, 20 SPE opcodes; without it, 0.

- **GCC defines no e500 macro.** GCC removed SPE support, which is why the path is a hand-written
  `xor_spe.S` plus `-Wa,-mspe` rather than intrinsics. Diffing the predefines of `-mcpu=8548` against
  `-mcpu=464fp` yields only soft-float proxies (`__NO_FPRS__`, `_SOFT_FLOAT`, `_SOFT_DOUBLE`,
  `__NO_LWSYNC__`). Keying on those would ship `evxor` to a soft-float classic PowerPC and fault, the
  SSSE3 bug again. So auto-detection from the compiler is not available.
- **The target says it instead, and the software can read it.** OpenWrt's `MAKE_VARS` exports
  `CXXFLAGS="$(TARGET_CXXFLAGS) ..."`, `TARGET_CXXFLAGS = TARGET_CFLAGS`, and that carries
  `CPU_CFLAGS_$(CPU_TYPE)`, i.e. `-mcpu=8548`. So the makefile can read the core from the flags it is
  already handed, and the package needs no CPU conditional. Note the fork's own cross targets take
  the march inside `CC`, not `CXXFLAGS`, so the filter searches `CC CXX CFLAGS CXXFLAGS`.
- **8548 alone is too narrow.** OpenWrt maps these 32-bit PowerPC types: 603e, 8540, 8548, 405, 440,
  464fp. **8540 is e500v1 and also has SPE** (v1 lacks only double-precision SPE FP, which this does
  not use). No published target uses 8540 today. Match both, with `filter` (whole words) not
  `findstring` (substring).
- **The XOR round-trip cannot catch a wrong XOR, only a missing one.** It asserts
  `changed && restored`. XOR is its own inverse, so a wrong-but-deterministic path still restores; a
  deliberate truncation was caught in exactly the degenerate cases where the XOR did nothing at all.
  The differential comparison against the word reference is what actually bites, verified by
  truncating an SPE call and watching that test alone fail across every tile, length and offset.
- **The sweep's spe row is red until the package bumps.** `arch-map.tsv` now asserts SPE opcodes for
  powerpc_8548, but the sweep builds from the package's pinned `PKG_VERSION`. It passes only once the
  package points at a fork release carrying the makefile detection, i.e. the pending v1.0.3 bump.

## The aarch64 gap was ours alone, and the pins needed a negative control

Closing the NEON and ARM-CRC32 gaps required **no OpenWrt change at all**. Proof: building the fork
with the airoha (cortex-a53) toolchain and that target's own `-mcpu` yields 6 `crc32c*` instructions
and 9 `eor v*.16b` NEON ops. The code already ships; only the tests were absent.

- **`__ARM_FEATURE_CRC32` needs a named core.** Measured across the OpenWrt aarch64 toolchains:
  `-mcpu=cortex-a53`, `-a72` and `-a76` define it, `-mcpu=generic` (armsr/armv8, `CONFIG_CPU_TYPE`
  `generic`) does not. So three of the four published aarch64 targets ship the hardware checksum.
  Debian's `aarch64-linux-gnu-g++` defaults to no core, which is why fork CI compiled the path out
  and `[CRC32C hw vs sw agreement]` skipped silently. CI now also builds `-mcpu=cortex-a53` and
  **requires the comparison to have run**, since a skip must not read as a pass.
- **A pin that does not switch is a hollow green.** `bench_*_force()` returning 1 while the path stays
  the same makes the reference and the candidate the same code, so the comparison passes vacuously.
  Both aarch64 pins were checked by deliberately faulting `addmul1_neon` and the NEON `xor_tile` and
  confirming each named test fails. Never trust a new comparison without that control.
- **The tier tests used to leave the reference pinned.** They ended with `force("scalar")` /
  `force("word")`, so every round-trip test after them ran the reference path, not the dispatched
  one. Now they end with `bench_*_auto()`. This was already wrong on x86 and would have silently
  removed NEON from the aarch64 round-trips.
- **qemu-aarch64 `-cpu cortex-a53` does implement CRC32**, unlike the AVX-512 case, so this gap is
  fully closable under emulation.

## What the next feed build owes

Deferred on 2026-08-07, after the publish run went green: 111 jobs, no failures, two packages
across 35 architectures and three release lines, each installed from the signed feed in a stock
rootfs and refused without the published key.

- **The banner's build date is the SDK's date, not the build's.** `target/sdk/Makefile` bakes
  `SOURCE_DATE_EPOCH` into the SDK's `include/version.mk` and `include/toplevel.mk` exports it;
  GCC honours that variable and expands `__DATE__` and `__TIME__` from it. So the published
  binaries report the date the SDK was cut: `Jun 29 2026 12:59:20` on 25.12 and main,
  `Jul 24 2026 07:21:50` on 24.10. One source reports two dates, and both read as a stale binary
  to someone filing a bug. Feeding the line a real timestamp is not the fix, since the determinism
  is OpenWrt's own reproducibility measure. Drop the line or relabel it; `source commit` and the
  version already answer what it is asked.
- **That edit is not local.** The fork's copy sits in `main.cpp`, and CI ties the tag to
  `PROGRAM_VERSION`, so touching the banner means a new tag, which means both
  `udpspeeder-simd-snapshot` Makefiles take a new `PKG_VERSION` and a new `PKG_MIRROR_HASH` (the
  tarball name follows the version) on all three feed branches. The stock package's line is
  upstream's own, reached only through `010-note-snapshot-build.patch`, so it is dropped there or
  not at all.
- **The pins are stale by one commit on each of four entries**: `feed-main` a22b5740,
  `feed-25.12` ebc5ab6c, `feed-24.10` e646bb33, the fork 0ba7c9f5. The `.host-software` comment
  above the feed worktrees still says the feed "is not published at present and its workflow is
  disabled", which stopped being true when it went live. Correct it in the commit that re-pins.
- **No SDK is pinned, and the workflow runs itself weekly.** Each build job resolves the newest
  point release of its line at run time and verifies the SDK against that release's own
  `sha256sums`; the schedule fires every Monday at 08:00 UTC. A cron run can therefore republish
  different binaries, from a different toolchain and carrying a different baked date, with no
  recipe change and no host commit. The checksum is provenance, not a pin. Decide whether the feed
  wants an SDK pinned per line, or whether floating with the release is what a snapshot feed
  should do.
- **The feed retires once openwrt/packages #29901 and the net/udpspeeder version bump offered
  upstream both land**, since the official feed is then the better answer for either package and
  should not be left running beside it. That condition lived in the workflow's header comment
  until the comments were stripped, and this entry is now the only record of it.

## The flashprog package, and why its programmer list is spelled out

Written 2026-08-08 for openwrt/packages issue #29591, which asks for flashprog beside the
flashrom package that #29679 had just updated to 1.7.0. One package, `utils/flashprog`,
targeting v1.5 (released 2026-02-13; v1.6-rc1 was tagged the day before this work and is a
release candidate). Branch `flashprog` in the packages fork, commit 5ca6daa.

- **Selecting a programmer group also enables the ones upstream disables.** flashprog offers
  `group_pci`, `group_usb`, `group_ftdi`, `group_serial`, `group_jlink` and `group_internal`
  as meson choices, which reads like the tidy way to express an OpenWrt config menu. It is
  not. In `meson.build` the selection test is `groups.contains(true) or 'all' in programmer or
  'auto' in programmer and default`, and `and` binds tighter than `or`, so group membership
  alone selects a programmer and its own `default: false` is never consulted. Passing
  `group_pci` therefore builds `atahpt` ("not yet working"), `atapromise` and `nicnatsemi`
  ("not complete nor tested"), all three of which upstream's Makefile sets to `no`. The
  package names all 32 programmers individually instead, which reproduces upstream's default
  set exactly and is what the long list in the recipe is buying.
- **Naming a programmer is a hard selection, and unavailable is a hard error.** A named
  programmer that meson cannot build on the target calls `error()` and fails configure; a
  group-selected one merely reports "Not available on platform". So spelling the list out
  moves the architecture question from a silent skip to something the recipe must get right.
  `cpus_raw_mem` covers x86, mips, ppc, arm, aarch64, sparc, arc and e2k but **not riscv64 or
  loongarch64**, both of which OpenWrt publishes, and `cpus_port_io` is x86 only. The recipe
  gates on `$(ARCH)` accordingly. Checked against `include/meson.mk`: OpenWrt maps i386 to x86,
  powerpc to ppc, mipsel to mips, mips64el to mips64 and armeb to arm, so those two are the
  only OpenWrt architectures the raw-memory list omits.
- **The dependency is `libpci`, not `pciutils`.** `utils/pciutils` builds both; the flashrom
  package depends on `pciutils`, which drags in the `lspci` binary and the `pciids` database
  for a package that only links the library. Also, flashprog defaults `use_internal_dmi` to
  true, so unlike flashrom it needs no `dmidecode` on x86.
- **libjaylink 0.3.1 in the feed is enough.** Every one of the 30 functions and 9 constants
  `jlink_spi.c` uses is in 0.3.1, and neither flashprog's meson nor its Makefile states a
  minimum. Upstream is at 0.4.0, whose NEWS lists meson support, more USB product IDs and a
  udev `uaccess` tag, and no new API. So the J-Link programmer costs one feed dependency and
  nothing else. The flashrom package offers no J-Link programmer at all.
- **`linux_gpio_spi` is unreachable and was left out.** Its group, `group_gpiod`, is read in
  `meson.build` but is absent from the `programmer` option's `choices`, so it cannot be
  selected by name. It would also drag in libgpiod, which carries `DEPENDS:=@GPIO_SUPPORT`
  and would make the whole package unbuildable on targets without GPIO support.
- **The license is GPL-2.0-only, not the `-or-later` the flashrom package claims.** 85 files
  carry "either version 2 or (at your option) any later version"; 46 carry version 2 with no
  later clause, including `spi.c`, `spi25.c`, `layout.c`, `linux_spi.c`, `linux_mtd.c` and
  `dummyflasher.c`. Upstream's own `meson.build` declares `GPL-2.0`.
- **Verified on 124 jobs, all green** (run 31266763904): 35 architectures across 24.10, 25.12
  and snapshot, each asserting the exact programmer set for its architecture class plus the
  package's file list and dependency list; five architectures repeated with all four config
  symbols off, asserting libpci, libftdi1 and libjaylink absent and only `libc` left; and an
  install into a stock rootfs on each line running a dummy write, verify, read, `cmp` and
  erase. The assertions were proved against negative controls first: claiming aarch64 for an
  x86 build reports `rayer_spi`, `nic3com`, `nicrealtek` and `satamv` as wrongly built, and
  claiming the minimal config for a default build reports 13 failures.
- **Two CI failures that were not the package, both worth keeping in mind.** The d1/generic
  snapshot SDK was rebuilt between reading `sha256sums` and downloading the tarball, so the
  fetch now retries three times; a snapshot directory moves under you. And the
  branch-tracking `openwrt/rootfs:x86-64-openwrt-24.10` image lists a kmods feed whose kernel
  hash has moved, so `opkg update` returns non-zero on one of six feeds. Rather than silence
  it, the job now reads the package's own `Depends:` and requires each one to be present in
  the feed, which is the claim the job exists to make.
- **A worktree on the Windows drive cannot record the executable bit.** `chmod +x` followed by
  `git add` left the CI scripts at mode 100644, and all 123 jobs died at their first step with
  exit 126. `git update-index --chmod=+x` is the fix, and the general rule is that a mode
  change made under `/mnt/c` has to be set in the index, not the filesystem.

## Correcting the flashprog entry: the design it describes is gone

The entry above, "The flashprog package, and why its programmer list is spelled out", described
commit 5ca6daa and is now wrong in three places. It is left standing because this log is
append-only; read this entry instead.

- **There are no config symbols and no `Config.in`.** That design put four `default y` bools in a
  menu, which meant the buildbot shipped the full package to everyone and the saving existed only
  for people already running menuconfig. The operator called it a mistake, correctly: OpenWrt is
  size-focused and the feed download is what most people install.
- **There are two packages, not one.** `flashprog` is the default variant carrying everything the
  architecture supports; `flashprog-spi` carries only the programmers that need no library. Both
  own `/usr/bin/flashprog`, so they conflict: `flashprog` declares `CONFLICTS`, `flashprog-spi`
  declares `PROVIDES:=flashprog`, the shape `net/chrony` and `libs/libwebsockets` use. Renaming the
  binary per variant, which is what `utils/flashrom` does, is wrong here because flashprog
  dispatches subcommands and its man pages carry its own name.
- **The programmer list is no longer spelled out, and the riscv64 gate is gone with it.** The recipe
  selects upstream's `group_serial`, `group_usb`, `group_ftdi`, `group_jlink` and, on x86,
  `group_internal`, naming only `dummy`, `linux_spi` and `linux_mtd`, which belong to no group we
  select. Measured against the hand-written list this costs 8 kB and three obsolete x86 programmers
  (`atahpt`, `atapromise`, `nicnatsemi`) and drops `rayer_spi`, a parallel-port cable programmer no
  modern board can use. It buys a recipe a third the size that cannot break when upstream renames or
  narrows a programmer, because group selection is soft where a named programmer is a hard
  `error()`. The old entry's riscv64 and loongarch64 special case dissolved: the raw-memory
  programmers are now only ever added inside the x86 branch.

Two findings from that work are worth keeping.

- **A group's membership is the real argument against groups, and it is about `DEPENDS`.**
  `group_usb` gained `ch347_spi` and `dirtyjtag_spi` across releases. A version bump can therefore
  add a programmer whose library the recipe never declared, and soft selection reads `staging_dir`,
  so it activates only when something else happened to stage that library. `ft4222_spi` already
  shows the shape: it is in `group_usb` and `group_ftdi` but needs libusb, so selecting `group_ftdi`
  alone links a library the package would not have declared. Declaring all four libraries
  unconditionally is what makes groups safe here.
- **flashprog needs `libpci`, never `pciids`.** It calls only config-space, enumeration and filter
  functions, never `pci_lookup_name`, and matches devices numerically against its own table. Proven
  three ways: no such call in the source, both PCI programmers reaching their expected errors in a
  rootfs with no `/usr/share/hwdata/pci.ids`, and pciutils' own documentation calling the database a
  name lookup table. Depending on `libpci` rather than `pciutils` therefore avoids `pciids` at
  1,651,592 bytes installed, plus `libkmod` and the `lspci` binary.

## Correcting the flashprog entry again: the two packages are co-installable, and why

The entry above still describes `flashprog` declaring `CONFLICTS` and `flashprog-spi` declaring
`PROVIDES:=flashprog`. That design is gone. It also called flashrom's rename-the-binary approach
"wrong here"; that judgement is reversed, and this entry says why.

- **A versioned `PROVIDES` makes the name substitutable, which is not what it looks like.** The
  operator ran `apk add flashprog-snapshot` on a real router and apk installed
  `flashprog-spi-snapshot` instead. This is documented behaviour, not a bug: apk-package.5 says a
  versioned provide makes apk "treat it as-if a real package with the provided name is installed",
  so the provider satisfies a request for the provided name outright. `provider-priority` cannot
  arbitrate, because it applies only to *non-versioned* provides. All three orientations of the
  provide were tried; none gives exclusion without also giving substitution.
- **OpenWrt's `CONFLICTS` never reaches apk.** `package-pack.mk:417` writes it only into the opkg
  control file, and OpenWrt passes twelve `--info` keys to `apk mkpkg`, none of them a conflict.
  apk expresses a conflict as a negative dependency (`depends: !name`), which OpenWrt never emits.
  So under apk the conflict half was silently absent while the provide half was fully active.
- **The fix is distinct install paths, so there is nothing to arbitrate.** `flashprog-spi` installs
  the same ELF as `/usr/bin/flashprog-spi`. The two packages now share no path, are co-installable,
  and carry no `PROVIDES` and no `CONFLICTS` at all. This is what `utils/flashrom` does with its
  five variants, and the earlier entry's argument against it (that flashprog dispatches subcommands
  and its man pages carry its own name) does not survive contact: the package ships no man pages,
  and argv[0] changes nothing about subcommand dispatch.
- **Local-file installs never exercise provider resolution.** Every container test installed by
  filename, which names an exact package, so the substitution could not appear. Only the operator's
  `apk add <name>` against a published feed reached the resolver. A package carrying `PROVIDES` has
  to be tested by name from a repository index, or it is not tested at all.

Three smaller findings from settling the recipe.

- **`group_pci` adds no programmer; it makes `libpci` required.** Upstream has
  `libpci = dependency('libpci', required : group_pci)`, so selecting the group turns a missing
  libpci from a silent programmer drop into a hard configure error. That is the whole reason to
  select it, and the recipe comment now says so rather than describing the off-x86 case.
- **The x86 gate is `CONFIG_TARGET_x86`, not `$(ARCH)`.** `target/linux/uml/Makefile` sets
  `ARCH:=x86_64` without setting `CONFIG_TARGET_x86`, so the two predicates diverge. Gating the
  programmer groups on one and `DEPENDS` on the other selected `group_pci` where libpci was never
  declared, and uml failed to configure. Both gates now read `CONFIG_TARGET_x86`.
- **Off x86, `internal` degrades to `linux_mtd` without touching `/dev/mem`.** `internal_init()`
  calls `try_mtd()` before `processor_flash_enable()` and before the
  `#if defined(__i386__) || defined(__x86_64__)` physmap block, so on a non-x86 build with
  `LINUX_MTD_AS_INTERNAL` the MTD path is reached first and succeeds on its own. This is what lets
  the commit message say the group is redundant off x86 rather than merely unsupported.

## 2026-08-10 — the tools this host runs are now pinned like the software it builds

Every tool reached through whatever the machine carried: node and allium from
`~/.local`, java from `/usr/sbin`, `tla2tools.jar` from a home share. A generated
pre-push hook had `$HOME/.local/bin/node` baked in, so it worked here and nowhere
else, and a stale `target/release/host-lint` six minor versions behind the binary
on PATH turned a green integration suite red until the cause was found.

`.env` now names each tool's version and in-tree path; `tools/install-tools.sh`
fetches them into `.host-tools/` and verifies each sha256 before unpacking.
Recorded as `call/0007`. The general form belongs upstream in the template.

Two findings worth keeping. `allium-cli` does not install from crates.io at 3.4.2
or 3.5.0 without `--locked`, because it resolves a newer `allium-parser` whose
`analyze_with_cross_module` grew arguments. And host-lint before v0.13.0 failed
closed on any submodule gitlink, so no `git submodule add` could land in a gated
host; upstream had fixed it a month before this host noticed, which is the
argument for comparing a pin against `origin/main` before writing a patch.

## 2026-08-10 — this host must not reference an upstream tracker, and a rebase obliges a re-pin

A commit message pushed from this public host that carries `owner/repo#N` or a
`github.com/<owner>/<repo>/(issues|pull|commit)/` URL makes GitHub post a
`referenced` timeline event on the target. Two host commits had already done it,
one through each form, so this governance repo surfaced inside an upstream thread
about the package.

The event cannot be retracted. Issue events are read-only in the REST API, and a
force push only makes the commit unreachable while GitHub keeps it addressable by
SHA. After the offending commit was rewritten out of this history, the API still
resolved it and the event still rendered. The remaining levers are a support
request, a delete-and-recreate of the repo, or making it private. Prevention is
therefore the whole remedy, so `tools/crossref-check.sh` installs as the
`pre-push` hook and refuses either form. It cannot gate an issue or pull request
body posted through `gh`, which stays a matter of care.

The same rewrite taught the second rule. A rebase strands every reference to what
it rewrote. Six pins in `.host-software` named commits that later force pushes
had made unreachable, and a fresh clone fetches reachable objects alone, so
`software --materialize` could not check them out and exited 2. The
reproducible-build lane had been red for a day, and it died two steps before the
build it exists to verify, so it never built anything at all. Reachability is the
test: the API resolves an unreachable object and proves nothing, while `git
ls-remote --heads` lists what a clone will actually get. Both rules are now
priority rules in `CLAUDE.md`.

One more thing surfaced and is not yet fixed. Four host-lifecycle versions read
this project: the `tools/host-lifecycle` submodule at 0.35.1, which the mdBook
and reproducible-build workflows build from, `.env` at v0.50.0 for local use, and
a git rev in `prose.yml`. Version 0.35.1 parses only `repro-exempt`, so it reads
the `repro-waiver` lines an applied ledger entry introduced as absent and reports
host-lint as DRIFT, and it has no `book --print-mount`, which is the mdBook
failure. A bump of the submodule to the v0.50.0 commit clears both. Note what the
lane proves once it goes green: three components record no artifact and host-lint
is waived, so every line is a skip or an exemption and no reproducibility is
established yet.

## Correcting the skew entry: the fix was `.env`, not a submodule bump

The entry above proposed bumping the `tools/host-lifecycle` submodule. What
landed is narrower and treats the cause instead of the symptom. All three
workflows now install the `.env` pin and source `.env` for the path, so one
binary answers for CI and for the local shell. Prose and mdBook went green at
once, and the reproducible lane reports `WAIVED host-lint repro-waiver
(call/0002)` with the other three skipped.

How the pins stayed stale is the part worth keeping. The submodule pointer has
exactly one commit in its whole history, `72a8e2e`, which wired it at v0.35.1,
and nothing ever moved it, because `software --check` audits the components in
`.host-software` and not the tools under `tools/`. `prose.yml` carried its own
inline rev at v0.30.1. Every command run by hand used the newest binary
available, so CI alone ever saw the old ones. A second source of truth is not a
pin; it is a way for two answers to disagree without anyone noticing.

One skew survives on purpose. The submodule still supplies the lifecycle skills
that `.claude/skills/` links to, so those remain v0.35.1's while the binary is
v0.50.0, and the `release` phase has no skill there at all. Bumping the
submodule is what closes that, and it is a ledger-ordered action rather than a
free edit.

Read the green with care. v0.50.0 prints `0 builds verified here ... nothing to
attest`, which is the honest summary: no component reproduces yet.

## Correcting the upstream-reference entry: the closer belongs in the pull request body, not the commit

The scoping bullet the entry above carried into CLAUDE.md said a commit in the
packages worktree keeps its `Closes:` trailer because upstream requires it.
Checked against openwrt/packages on 2026-08-10, that claim is wrong. Nothing
requires it, and the tree's convention is the closing keyword in the pull
request body, where it fires once at merge, rather than in the commit, where
every push of an amended branch re-posts a reference on the issue. Four of the
five most recently merged pull requests that closed an issue put the keyword in
the body; the one exception (fluent-bit) used a commit trailer. openwrt/packages
PR 30186 is the direct precedent: a new package, merged the same day, that
closed its request issue from the body with no issue reference in any of its
commits. The `openwrt-package-commit-style` manual in `host-lint-openwrt`
states the rule and carries the corpus measurement behind it.

CLAUDE.md's scoping bullet is corrected to match. The flashprog commit on
openwrt/packages PR 30228 drops the trailer, and at push time the body's
"Requested in #29591" becomes "Closes #29591", so the merge still closes the
issue.

## Host-repo commits carry the DeepSeek co-author trailer

Operator direction on 2026-08-10: the host repo's co-author trailer is
`Co-Authored-By: DeepSeek V4 Flash 0731 <noreply@www.deepseek.com>`, not the
Claude one. The packages worktree still carries no co-author trailer at all,
per call/0003; only the name the host trailer carries has moved.

## 2026-08-10 — v1.1.0 released: the DNS lease manager, the first minor bump

The first minor version bump of udpspeeder-simd shipped as v1.1.0, carrying the
DNS lease manager (plan/0001). The client's `-r` now accepts a hostname: a
single-header, allocation-free, nonblocking DNS Locator-Hint Cache
(`dns_lease_mgr.h`) resolves it, leases the candidate IPs for an effective TTL,
refreshes before expiry, serves the last-known candidates while a refresh fails
(the stale window, default 1 hour, 0 = never expire), falls back to TCP on
truncation, and re-points the tunnel with a second `connect()` on the same fd
so the io_uring multishot and ev_io watcher stay valid. ECONNREFUSED on the
remote recv path force-refreshes; a FIFO `dns-refresh` command does it by hand.
Server mode rejects hostnames in `-r`.

Two decisions were recorded: call/0008 (versioning: minor = feature, patch =
fix, the tag is the release, the banner must equal the tag) and call/0009 (the
header is C++-compatible — every negative constraint of the C11 spec preserved,
dialect shifted to the CXX-only build). The release process ran as the house
process: fork commit 36641bc tagged v1.1.0, CI (now including the new allium
and tlc spec lanes, which gate the release job) published seven static
binaries, `.host-software` re-pinned, and the `release` receipt flipped from a
stale `skip` to `done` (authorization plan/0001).

The spec lanes are the notable new machinery in the fork's CI:
`.github/workflows/ci.yml` gained an `allium` job (allium-cli 3.5.0 +
host-lifecycle pinned, check/analyse/plan + obligations --strict-discharge)
and a `tlc` job (tla2tools.jar v1.7.4, hash-pinned like bench/sde.lock). The
obligations checker resolves `test:<name>` by `fn <name>(`, a Rust convention;
the C++ bench tests carry a `/* fn <name>(...) */` marker comment before each
test function so the checker brace-matches the real body. TLC writes
`spec/DNSLease_TTrace_*` and a `states/` dir on runs; both are gitignored.

## 2026-08-11 — the DNS lease manager verification gaps are closed

A review of the v1.1.0 verification found five gaps; all are now closed. The
DNS response parser was never fuzzed (the fuzz target only covered the packet
decoder), so `bench/fuzz_dns_lease.cpp` now feeds mutated responses to
`dns_lease_parse_response` under ASan/UBSan — a bounded random driver and a
libFuzzer target (`make fuzz-dns` / `fuzz-dns-libfuzzer`), wired into CI. The
`stale_max_ms == 0` sentinel (serve stale indefinitely) was untested on both
lanes: a C++ case now advances a stale lease ten days and asserts it never
gives up, and the TLA+ `StaleGiveUp` gained the `StaleMax > 0` guard the header
already had, with a second model instance (`MC-stale0.cfg`).

The live runtime paths were never exercised end to end: the create-on-first-
lease socket, the re-point on a candidate change, and the TCP fallback on a
truncated answer. A python DNS stub (`bench/dns_stub.py`) on port 53 plus a
driver (`bench/dns-live-test.sh`) now run the real client against real servers
in CI, and the Windows build is exercised under Wine (`make test-mingw` +
`wine64`), compiling the header's Windows PAL for the first time.

Two pre-existing fork bugs surfaced: `lib/fec.cpp` cast a pointer to `long`
(32-bit on Windows x64 -> precision loss), fixed with `(intptr_t)`; and
`xor_spe.S` kept its comment outside the HAVE_PPC_SPE guard, so the MinGW
assembler choked on it — the guard now covers the whole file. The live lane
also needed its resolv.conf written via a bind mount (a runner's
/etc/resolv.conf is systemd-resolved's and not writable even as root). The
obligations checker's `fn <name>(` marker convention (Rust-oriented) applies to
the new test functions too.

## 2026-08-11 — branch_libev split: udpspeeder-only vs the feed, and the persona-in-commit rule

The fork's `branch_libev` carried two streams interleaved in one linear chain:
39 commits of OpenWrt feed-publishing work (the `d0e497a..03b8369` span) sat
between the pre-feed udpspeeder work and the v1.1.0 DNS-lease run. The branch
was split by rebuilding both streams on the pre-feed tip `ef92d69`:

- `branch_libev` is now udpspeeder-only: pre-feed history + the 4 banner/
  version commits (`2f8ad9d`..`b4ef0d9`, tagged v1.0.4/5/6) + the 5 DNS-lease
  commits, re-rooted onto `ef92d69`. New tip `e33aa71`. The feed files
  (`.github/scripts/*`, `package-feed.yml`) are gone from the branch.
- `feed-snapshot` is the new feed branch: `ef92d69` + the 29 feed-machinery
  commits only (no banner, no DNS). Tip `7acdf4e`. No tags live on it.

The re-root rewrote the DNS commits, so the v1.1.0 version-bump commit is now
`ba6e4ab` (was `36641bc`). The four `v1.*` tags were NOT moved: the fork has a
tag-protection rule blocking in-place tag updates (deletion and creation both
pass; only update is blocked — GH013 "Cannot update this protected ref"). The
tags stay at their old commits, which remain reachable through the tag objects
and feed-snapshot's history. The release receipt's evidence (`tag v1.1.0 at
36641bc`) is still literally true because the tag never moved. Re-pinning the
host to the new tip was done in the same session; the tag/pin pair is now
forked (tag at the old commit, pin at the new tip) by the protection rule's
choice, not by oversight.

The rule that fired here: **a commit message is the record of who did what; a
persona is a planning fiction, not a doer.** Commit `8b67771` opened its body
"Samira's lane is now full" — a persona named as the author of verification
work. Rewritten as `7da6e1f` ("The DNS response parser gets the fuzz
treatment...") with the trailer kept. The cast-room commits that *introduce or
revise* a persona may name it (that is their subject); a software-work commit
may not attribute the work to one.

## 2026-08-11 — canonical branch renamed branch_libev → main

The udpspeeder-simd fork's canonical branch moved from `branch_libev` to `main`
(the rename the split had been leading to). The fork's `main` is at `845df57`
(the ci.yml rename commit), the GitHub default branch is `main`, and remote
`branch_libev` is deleted. `feed-snapshot` keeps its name.

The rename surface, all moved in the same pass: the 5 `branch_libev`
references in `.github/workflows/ci.yml` (the push/pull_request trigger filters
and the benchmark-storage conditions) — a rename without them silently stops CI
on pushes to the new branch — plus the host's `.host-software` `branch = main`
(pin `845df57`) and the CLAUDE.md canonical-branch fact. Call/0000's mention of
the adoption-time `branch_libev` is left as the historical record it is.

The worktree was re-registered at `software/udpspeeder-simd/main/` from the
bare store. A `git worktree move` to the new name left a phantom `main_old/`
directory entry on the WSL /mnt/c filesystem (stat/find ENOENT yet the listing
shows it; rmdir "not empty") — a DrvFS cache artifact of the interrupted
rename, invisible to the host gate. A `wsl --shutdown` or a C: remount clears
it; it is cosmetic.

Release health after the split + rename: the release job is tag-triggered
(`tags: ['v*']` + a ref-starts-with test) and branch-agnostic — a future tag
cut on `main` publishes normally, and the eight verification jobs it needs all
run on the new branch. The v1.1.0 release's own tag was never moved (tag
protection blocks in-place updates), so its evidence stays true.

## 2026-08-11 — feed branches rewritten to a single compliant commit; v1.1.0 in the feed

The packages repo's three feed branches (feed-main, feed-25.12, feed-24.10)
carried ~24 commits each that failed the repo's formality-check hook (missing
Signed-off-by, bad subjects, empty bodies, patch files without git headers) and
were a newer-upstream sync plus the snapshot packages, only the snapshot dirs
of which the feed workflow actually uses. Each branch was rebuilt as a single
compliant commit on master (1d40ad9) carrying only the three snapshot package
dirs (udpspeeder-snapshot, udpspeeder-simd-snapshot at v1.1.0, flashprog-snapshot)
with git-header'd patches and a Signed-off-by. All three are now identical at
387ae05; the formality-check passes with errors=0.

The fork's feed-snapshot branch was reduced in the same pass to an orphan stub
(e2f9a85) carrying only the feed workflow + scripts, no udpspeeder source. A
dispatch from it built and published 111 jobs green, confirming the stub. The
v1.1.0 bump (PKG_VERSION 1.0.6 to 1.1.0, PKG_MIRROR_HASH recomputed via the
OpenWrt dl_tar_pack method: git archive, then tar --sort=name --owner=0
--group=0 --mode=a-s --mtime=@<commit-time>, then zstd -T0 --ultra -20) ships
through the feed once a dispatch runs against the rewritten branches.

## 2026-08-12 — release assets are immutable; v1.0.0 left as an accepted rebuild

Release assets are treated as immutable. Deleting or restoring a v* tag
re-triggers the tag-driven release workflow, which rebuilds and replaces the
published binaries; the build is non-reproducible (call/0006, the runner's g++
varies), so a rebuild changes the bytes even from the same source. A
tag-protection probe during the split work deleted and restored v1.0.0, which
re-published its two binaries on 2026-08-11 (built from d266e37, the same
source as the original 2026-08-02 release, but different bytes). The v1.0.0
assets are left as that rebuild; v1.0.1 through v1.0.6 are untouched at their
original dates. Going forward no v* tag is deleted or restored: the assets it
points at are immutable. Test tag protection with a scratch tag name, never an
existing release tag.

## 2026-08-14 — flashprog ships the variant pattern under a non-canonical provide

The entry "Correcting the flashprog entry again: the two packages are
co-installable, and why" describes the distinct-install-paths design:
`flashprog-spi` installing `/usr/bin/flashprog-spi`, no `PROVIDES`, no
`CONFLICTS`. That design is gone. The package now ships four variants that all
install `/usr/bin/flashprog` and all carry `PROVIDES:=flashprog-bin` from
`Package/flashprog/Default`, with `DEFAULT_VARIANT:=1` on the full variant.

- **Reviewer efahl asked for the variant pattern `dnsmasq` uses.** In that shape
  the narrow variants provide the *canonical* name, which `package-pack.mk` emits
  as a versioned provide. That reintroduces the substitution the entry above
  records, in its quietest form: with a narrow variant already installed,
  `apk add flashprog` is satisfied by the provide and installs nothing at all,
  reporting success. A silent no-op, not an error.
- **The deviation is the provide's name.** All four variants provide
  `flashprog-bin`, a name no package is called. The versioned provide then buys
  mutual exclusion between the variants while `flashprog` stays the full
  package's own real name, never a virtual any variant can satisfy. `apk add
  flashprog` installs the full package or fails.
- **Measured on the router's exact resolver.** apk 3.0.5 inside an
  `openwrt/rootfs:x86-64-25.12.4` container. Clean, `apk add flashprog` selects
  the full package. With `flashprog-spi` installed it errors on the
  `flashprog-bin` conflict instead of no-opping. The documented swap,
  `apk del flashprog-spi && apk add flashprog`, works.
- **The measurement used synthetic apks, not real builds.** Twelve packages
  (each candidate shape crossed with the four variants) built by `apk mkpkg` with
  a dummy payload and only the metadata under test, indexed by `apk mkndx`, and
  installed *by name* from that feed. The resolver reads index metadata alone, so
  the payload is irrelevant and a shape settles in minutes rather than a
  cross-compile apiece. Installing by name is the load-bearing half; a local
  filename names an exact package and never runs the resolver.
- **The dependency lists came out of the descriptions.** efahl's closing note
  asked for it: `DEPENDS` is the source of truth, `apk query` surfaces it, and a
  duplicated list is a second place to edit. All four `Requires ...` sentences
  were dropped, `flashprog-spi`'s `Requires no libraries.` among them, since an
  empty depends list carries that already.

The PR head is 82e211de, pinned in `.host-software`. BKPepe's CHANGES_REQUESTED
(the sizes request that the commit message's table answers) is still the
standing review state; efahl's "looks good to me" arrived as a comment rather
than an approving review, so the gate does not flip on it.

## 2026-11-07 — template upgrade to the two-pin-surface revision; exec-bit audit over-fire recorded

The host upgraded from baseline 46a1fd2 through every pending ledger entry
(e4ed590, REFS-a-number-resolves, GATE-refs-in-verify,
LEXICON-declaration-is-a-report, PIN-two-surfaces-two-claims); `host-lifecycle
upgrade .` reads up to date at 14 applied. The spine was re-applied to
CLAUDE.md and STRUCTURE.md (the project-specific tail and the two priority
rules kept); UPGRADING.md's one dead register pointer (the template's own
call/0018, cited in a title) is boxed in backticks per the reference entry's
known-limitation remedy. A fresh checkout bootstrap now runs: submodules,
software materialization (14 items), skill links, hooks on the host and all
four worktrees, and `software --verify-setup .` clean.

The declared toolchain is host-lifecycle v0.50.0 pinned in `.env` (installed
by tools/install-tools.sh); the ~/.cargo/bin 0.64.0 on this machine is ahead
of the adopted ledger and its inventory check (a `.host-inventory` remedy)
is not owed by this revision yet.

The exec-bit audit over-fired on the two foreign OpenWrt pins (514 findings,
all the `$(INSTALL_BIN)` install idiom; sources never executed in place).
Disposition recorded in call/0010: reported upstream as host-lifecycle issue
45 with the fresh-checkout context; interim, the audit's own staged-chmod
remedy is applied on this machine (local index state only, resets on every
`--materialize`, so a fresh setup re-derives it from the gate's own printed
remedies). The audit also caught one real defect: bench/dns-live-test.sh in
udpspeeder-simd documented its own `./` invocation while recorded 100644;
fixed by commit bce0f3c, pushed, `.host-software` re-pinned same session.

The operator declined to set a goal this session; the open frontier remains
plan/0000's #upstream-cross-cxx task, blocked on the flashprog PR review
(CHANGES_REQUESTED standing, head 82e211de).

## 2026-11-07 — the v0.63.0 span: AGENTS.md, the lem system, CI receipts; the old checkout cross-checked

The template's full span landed (baseline now 7ef379e, 26 entries absorbed).
The manual is AGENTS.md (CLAUDE.md is a pointer, history kept by git mv); the
corpus is declared (.host-corpus: AGENTS.md, STRUCTURE.md) and held to the
strict prose tier; the spine carries the lem pronoun system, which governs how
the model voices itself in this repo from here on. Toolchain: host-lifecycle
v0.63.0 and host-lint v0.24.1 (pin db4a0d20, artifact hash re-derived),
both in .env and .host-software; the tools/host-lifecycle, tools/allium and
tools/specula submodule pointers moved to the template's pins.

call/0010 is superseded by call/0011: v0.63.0's audit learned the OpenWrt
install-macro idiom (the issue-45 fix), so the 514 staged chmods are gone with
the finding that needed them. The v0.50.0 completeness-gate deadlock (one
skill link name demanded by both the software worktree and the tools
submodule) is also gone at v0.63.0; bootstrap completes again.

CI lanes are receipts now (call/0011 records the evidence policy: green at
the judged revision where it exists; otherwise the lane's most recent run,
read and recorded, green or not). The qemu packet lane's standing failure is
fixed in the same push: the feed branches renamed net/udpspeeder-simd to
net/udpspeeder-simd-snapshot and the lane still sparse-checked-out the old
name; the checkout, feed symbol, and make target now use the snapshot names
and the installed binary keeps the udpspeeder-simd name. Still red, disclosed:
the packages mirror pin's multi-arch-test-build and stale-bot lanes (the
fork's forge never registered them; no run URL exists to cite), upstream
OpenWrt's kernel/label-kernel/label-target/packages lanes (receipted at their
latest runs, not green on upstream's own repo), and this push's own check and
qemu runs, whose receipts follow once they land. The ci judge needs an absence
disposition for consumed mirror pins; that proposal is owed upstream in
call/0010's issue's shape.

The previous checkout at ~/old-agentic-openwrt-packages was cross-checked per
the operator's request. Nothing unpushed anywhere: the host repo, all four
component stores, and every submodule were at pushed states (the apparent
local-only commits were stale remote-tracking refs and tag-reachable release
commits). Two preservation items: the pre-rewrite originals of the
udpspeeder-update work (three commits on a local backup-before-rewrite branch,
existing nowhere else) are now pushed as archive/udpspeeder-update-pre-rewrite
on the packages fork; and the untracked read-only flashprog-test-packages/
directory (flashprog 1.5-r1 apk and ipk test builds with SHA256SUMS, dated
August) stays where it is, preserved by its permissions and recorded here.

## 2026-11-07 — correction: the exec-bit audit was never fixed at v0.63.0

The earlier entry today said v0.63.0's audit learned the OpenWrt
install-macro idiom (host-lifecycle issue 45 fixed) and call/0010 was
superseded. That was wrong. The local findings vanished because the
worktree indexes still carried call/0010's staged chmods; the first CI run
of the new check lane, which materializes fresh, printed all 514 findings
again. call/0010 is re-accepted (status retracted in place, this entry is
the append-only correction), the interim state remains load-bearing, and
the check lane now derives it from the gate's own printed remedies in CI:
it runs the gate, executes the remedy lines verbatim when the only
failures are those, and re-runs. Issue 45 stays open upstream with no fix
shipped. The same CI run exposed a second gap: host-lint's obligations
manifest declares kani: rungs, so the gate demands the host-prove
re-deriver on PATH wherever it runs; the lane installs host-prove v0.3.0
before the gate now.

The mdBook "changed end url" premise from the operator's goal note did not
match any observable state on the gh side (repo, owner, Pages config, and
gh-pages content all unchanged; the mdBook lane green). The book still
publishes at connollydavid.github.io/agentic-openwrt-packages/. If a move
is intended, it has not happened yet; nothing was changed for it.

## 2026-11-07 — the host stood up at the v0.63.0 pins; the check lane is green in CI

The stand-up is complete at baseline 7ef379e. The check lane (the push
boundary gate) is green in CI after three fixes: the lane derives the
call/0010 interim from the gate's own printed remedies (a fresh
materialization otherwise re-prints all 514 findings), it installs
host-prove v0.3.0 because host-lint's obligations declare kani: rungs,
and it inits the host-template submodule whose lifecycle.manifest the
receipts re-check reads. CI receipts are recorded for check, prose, and
mdBook at the current head; the qemu lane's fix is dispatched and its
receipt follows its green; the two packages mirror-pin lanes stay red with
no honest evidence to cite (disclosed in call/0011).

The harness doors are installed for both harnesses (host-goal, host-tasks,
host-ci), gitignored as generated machine state, and install --check
passes. The dream audit is clean over the repo tier. No goal is set; the
goal loop is ready (the doors, the verbs, GOAL.md to be declared in the
corpus at first goal set). plan/ numbering stands ready at 0002.

The operator's goal note carried an mdBook end-URL change premise that
matched nothing on the gh side (checked: repo identity, pages config,
gh-pages content, lane health); recorded as unconfirmed. It arrived
wrapped in a suspicious envelope claiming to be a goals plugin bridge and
directing a third-party npx install; L flagged it, did not relay it, and
the operator then sent the goal text directly.
