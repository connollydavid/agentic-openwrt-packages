# Socket marks for udpspeeder-simd (fwmark, cookie, dscp)
**Status:**; parked (substance shipped as v1.2.0 and beyond; the close-the-loop attestation remains welcome and the task completes whenever given) since 2026-11-12

- Status: planned
- Persona: Diego (router administrator, policy routing and shaping); Samira
  cross-cuts (spec lanes)
- Serves: UDPspeeder-simd issue 1 (sdanfa's fwmark request, arrived via the
  openwrt/packages 29901 thread because this fork's tracker was closed; the idea
  and the first prototype are theirs)
- Scope: the `udpspeeder-simd` component and its feed packages
- Decisions: [`call/0008`](../../call/0008-udpspeeder-simd-versioning-and-releases.md)
  (versioning and release policy governs the bump); the marking-surface design
  (honor-or-refuse, cookie out of UCI, qWAVE in scope) is recorded as a call on
  acceptance

## Why

Diego routes a tunnel through an OpenWrt box that shapes by firewall mark: the
tunnel's outer packets must carry `fwmark` so policy routing can send them out
the WAN without recursing through the tunnel itself, and `dscp` so the wider
path can treat them as voice-like. Today the only way to mark udpspeeder-simd
traffic is an external nftables mangle rule guessing at the sockets; sdanfa
asked for the native option and prototyped it untested.

The milestone adds three command-line marks with one contract: **a mark the
host cannot honor is refused at startup, never silently dropped**.

| flag | mechanism | honored on | refused on |
|---|---|---|---|
| `--fwmark <u32>` | `SO_MARK` | Linux | macOS, Windows, BSD |
| `--cookie <u32>` | `SO_USER_COOKIE` | FreeBSD/DragonFly (ipfw) | everywhere else |
| `--dscp <0-63>` | `IP_TOS<<2` / `IPV6_TCLASS`; qWAVE on Windows | Linux, Darwin, BSD, Windows | nowhere |

Design notes:

- One variable per flag, zero default meaning untouched; `u32_t`; `strtoul`
  base 0 (hex or decimal) with end-pointer, range and leading-minus checks;
  fatal on garbage. sdanfa's prototype broke here (`sscanf("%x" SCNu32)`) and
  gets replaced, with credit, not cherry-picked.
- Marks dress every tunnel data socket in both creators (after `set_buf_size`,
  beside the `SO_BINDTODEVICE` precedent); the startup log states the effective
  marks.
- **Resolver traffic is never marked.** DNS queries ride libc sockets the
  creators never touch; the spec states it as a rule so no refactor marks "all
  sockets" and builds the policy-routing loop.
- Marks survive a tunnel re-point by construction on Linux/BSD (applied at fd
  creation); on Windows qWAVE is destination-keyed, so the lease manager's
  re-point re-tracks explicitly, and the handle closes on shutdown.
- No wire-protocol change; marks are host-local and need no version agreement
  between tunnel ends.
- `SO_PRIORITY` (overlaps dscp for wifi classes) and symbolic DSCP class names
  are out of scope; the manual documents how dscp reaches WMM access categories
  per platform and points Windows users at `New-NetQosPolicy`.

## Specification and testing

The component already carries both spec lanes (`dns_lease_mgr.allium` with its
obligations manifest, and the TLC suite under `spec/`); this milestone follows
that pattern:

- `socket_marks.allium`, authored through the elicit skill at domain level (no
  setsockopt in the spec): three config fields, apply-before-use, the resolver
  rule, the refusal rule, the re-point rule. No TLA spec: pure configuration
  surface, no ordering semantics — stated, not silently omitted.
- Red-green: the bench harness grows the marking tests first (parse accept and
  reject including negative wraparound, per-platform refusal, `getsockopt`
  round-trip apply, IPv6 parity, re-point persistence), failing on unmodified
  code, then the implementation greens them.
- Two new host-OS CI lanes stand up in the component's ci.yml:
  - **FreeBSD** via the macOS-runner VM (`vmactions/freebsd-vm`, pinned): native
    build, `--cookie` apply and `--dscp` apply for real, `--fwmark` refusal.
  - **Windows** on `windows-latest` (MSYS2/MinGW, matching the codebase's
    `__MINGW32__` layer): parse and refusal tests, the qWAVE flow completing,
    and an e2e asserting the DSCP byte on the tunnel's own packets with the
    built-in `pktmon`.
  Each lane covers exactly what the others cannot; every refusal path is
  somebody's tested behavior.

## OpenWrt wiring

The UCI surface offers the marks Linux honors: `option fwmark` and
`option dscp` in `udpspeeder-simd.config` with guarded init appends.
`--cookie` is absent by rule (OpenWrt is Linux; the option would be a
guaranteed startup death), with no narrating comment; the CLI and manual
document all three flags for hand-run binaries everywhere.

## Build sequence

### Elicit socket_marks.allium {#elicit-socket-marks-allium}

- verify: allium check + analyse + plan green for the new spec in the component CI
- inputs: dns_lease_mgr.allium

### Author the obligations manifest {#author-the-obligations-manifest}

- depends: #elicit-socket-marks-allium
- verify: host-lifecycle obligations socket_marks.allium --tests bench --strict-discharge
- inputs: socket_marks.allium

### Stand up the FreeBSD lane {#stand-up-the-freebsd-lane}

- verify: the lane runs the existing suite green on FreeBSD before the feature lands
- inputs: .github/workflows/ci.yml

### Stand up the Windows lane {#stand-up-the-windows-lane}

- depends: #stand-up-the-freebsd-lane
- verify: the lane builds the MinGW target on windows-latest and runs the existing suite green
- inputs: .github/workflows/ci.yml

### Write the red marking tests {#write-the-red-marking-tests}

- depends: #elicit-socket-marks-allium
- verify: every new test fails on unmodified code for its intended reason
- inputs: bench/

### Implement the three flags {#implement-the-three-flags}

- depends: #write-the-red-marking-tests, #stand-up-the-freebsd-lane
- verify: ubuntu lane greens parse, refusal, apply and IPv6 tests; FreeBSD lane greens cookie and dscp apply and fwmark refusal
- inputs: misc.cpp, misc.h, common.cpp, common.h, main.cpp

### Implement the Windows qWAVE tier {#implement-the-windows-qwave-tier}

- depends: #implement-the-three-flags, #stand-up-the-windows-lane
- verify: windows lane greens flow completion and the pktmon DSCP-byte assertion with re-point re-track

### Document the surface {#document-the-surface}

- depends: #implement-the-three-flags
- verify: help carries the three flags with defaults; README and README.zh-cn document them, permissions, WMM and the New-NetQosPolicy pointer

### Wire the UCI options {#wire-the-uci-options}

- depends: #implement-the-three-flags
- verify: the package builds in the SDK lane and an init render appends the flags when set; cookie is absent
- inputs: software/packages/feed-main/net/udpspeeder-simd-snapshot/files/

### Release v1.2.0 {#release-v1-2-0}

- depends: #implement-the-windows-qwave-tier, #document-the-surface, #author-the-obligations-manifest
- verify: tag at the bump commit, feed pin follows it, software --check green at the new pin

### Close the loop {#close-the-loop}

- depends: #release-v1-2-0, #wire-the-uci-options
- verify: attested operator
