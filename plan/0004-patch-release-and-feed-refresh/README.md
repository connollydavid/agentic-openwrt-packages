# v1.3.1: a release that matches the front door, and the feed MR that follows
**Status:**; planned; active goal since 2026-11-14

- Status: planned
- Persona: Diego (installs the release binary and waits on the feed package);
  Ingrid (holds the version, the mirror hash and the notices to packaging
  truth); Samira (holds every pin and receipt to its evidence)
- Serves: everyone who reads the release page instead of the repository tip,
  and the sdanfa thread on openwrt/packages whose package request is answered
  by the current release
- Scope: a patch release of the `udpspeeder-simd` component (version bump,
  man regeneration, tag, published assets), the host re-pin and release
  receipt, the feed MR's version and hash, and the operator reply that
  follows the MR update; no behavioural code change

## Why

The v1.3.0 tag built its assets at `3aee5a9`, and the documentation that
matter moved past the tag afterwards: the writing-whip pass and the
six-persona readthrough rewrote both READMEs, the guides, the glossary and
the man page after the release page was minted. A visitor who arrives at the
releases page today reads the pre-review front door while the repository tip
carries the reviewed one. A patch release closes that gap, and a version bump
is the only honest carrier for docs this prominent.

Two smaller truths travel with it. The READMEs' download example verifies a
literal sha256 recorded for the v1.3.0 asset while downloading through the
`latest` URL, so the example would contradict itself the moment v1.3.1
publishes; the example steadies to a form that cannot drift. And the feed MR
(openwrt/packages PR 29901, the package request from sdanfa's thread) still
pins `1.0.0`: DNS lease following, socket marks, the man page and the whole
reviewed documentation arrive only when the MR moves to `1.3.1` with its
mirror hash recomputed by the recorded `dl_tar_pack` method. The operator's
reply in that thread waits until that update lands, per the ruling.

## Build sequence

### Bump and regen {#bump-and-regen}

- verify: `make -C software/udpspeeder-simd/main -s man >/dev/null 2>&1 && ./software/udpspeeder-simd/main/udpspeeder-simd -h 2>&1 | grep -q 'v1\.3\.1' && grep -q 'v1\.3\.1' software/udpspeeder-simd/main/doc/udpspeeder-simd.1`
- inputs: software/udpspeeder-simd/main/main.cpp, software/udpspeeder-simd/main/doc/udpspeeder-simd.1, software/udpspeeder-simd/main/README.md, software/udpspeeder-simd/main/doc/README.zh-cn.md

Bump `PROGRAM_VERSION` to `v1.3.1`, regenerate the man page through the
recorded `regen = make man` so bump and derived page share one commit, and
replace the literal-checksum download example in both README twins with a
form that verifies without pinning a per-release hash.

### Tag and publish {#tag-and-publish}

- depends: #bump-and-regen
- verify: `gh release view v1.3.1 --repo connollydavid/UDPspeeder-simd --json assets --jq '.assets | length' | grep -qx 10`

Annotated tag at the bump commit (resolved through `rev-parse 'v1.3.1^{}'`),
pushed; the tag-triggered workflow builds the ten assets. The tag is never
deleted or restored afterwards: assets are immutable.

### Re-pin the host {#re-pin-the-host}

- depends: #tag-and-publish
- verify: `.host-tools/bin/host-lifecycle software --check .`
- inputs: .host-software

Record the new pin in `.host-software`, push the host, and let the release
ledger carry the migrated skip already cited to call/0006.

### Carry the feed MR {#carry-the-feed-mr}

- depends: #tag-and-publish
- verify: `bash tools/mirror-hash.sh https://github.com/connollydavid/UDPspeeder-simd.git v1.3.1 | grep -qx "$(sed -n 's/^PKG_MIRROR_HASH:=\([0-9a-f]*\)$/\1/p' software/packages/udpspeeder-simd/net/udpspeeder-simd/Makefile)"`
- inputs: software/packages/udpspeeder-simd/net/udpspeeder-simd/Makefile

Materialize the `udpspeeder-simd` branch as a recorded worktree line, bump
`PKG_VERSION` to `1.3.1`, recompute `PKG_MIRROR_HASH` with the `dl_tar_pack`
method (git archive, sorted tar with uid/gid/mode normalization and the
commit-time mtime, zstd ultra-20) behind a small `tools/mirror-hash.sh` so
the check re-runs, push the branch, and let the PR update itself.

### Advance the feed branches {#advance-the-feed-branches}

- depends: #carry-the-feed-mr
- verify: `grep -qx 'PKG_VERSION:=1.3.1' software/packages/feed-main/net/udpspeeder-simd-snapshot/Makefile software/packages/feed-24.10/net/udpspeeder-simd-snapshot/Makefile software/packages/feed-25.12/net/udpspeeder-simd-snapshot/Makefile && grep -qx 'PKG_MIRROR_HASH:=a8284ef9436663a82805051ca0bf2ab5fb09bd95cebc59b4877555c860ea65ab' software/packages/feed-main/net/udpspeeder-simd-snapshot/Makefile software/packages/feed-24.10/net/udpspeeder-simd-snapshot/Makefile software/packages/feed-25.12/net/udpspeeder-simd-snapshot/Makefile`
- inputs: software/packages/feed-main/net/udpspeeder-simd-snapshot/Makefile, software/packages/feed-24.10/net/udpspeeder-simd-snapshot/Makefile, software/packages/feed-25.12/net/udpspeeder-simd-snapshot/Makefile

The published feed is the delivery channel until the MR merges; its three
release-line branches each carry the snapshot package at 1.1.0. Each branch
takes its own version-bump commit with the recomputed mirror hash -- separate
branches, separate commits -- and feed-main's fwmark-and-dscp UCI wiring is
carried to the two release lines so 1.3.1 ships there with the options its
init script already maps. The recipe pins follow, then a dispatch rebuilds
the published feed.

### The operator reply in the 29901 thread {#the-operator-reply-in-the-29901-thread}

- depends: #carry-the-feed-mr
- verify: attested operator

The draft is ready; it is posted only after the MR update lands, per the
operator's ruling.
