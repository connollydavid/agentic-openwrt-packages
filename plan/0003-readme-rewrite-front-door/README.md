# README rewrite: the front door for our own software
**Status:**; active goal since 2026-11-13

- Status: planned
- Persona: Diego (primary reader -- installs, configures, watches it run);
  Ingrid (reads it for packaging truth); Samira (holds its claims to evidence)
- Serves: every new visitor to the repository, and sdanfa's class of user who
  arrives with one feature in mind
- Scope: the `udpspeeder-simd` component's two READMEs and the marks guide,
  with new mermaid diagrams and an elaborated SIMD section; no code, no release

## Why

The READMEs are still upstream's: their structure, their diagrams, their
story. The software underneath stopped being upstream long ago -- the SIMD
kernels, the DNS lease manager that follows a moving endpoint, the socket
marks with their honor-or-refuse contract, four-host CI that reads the
priority byte off the wire, the OpenWrt packages, the renamed binary. A
visitor reading the front door meets wangyu-'s UDPspeeder with footnotes,
not the software they would actually run. The Chinese README compounds it:
a translation of the old English one, one version behind even that.

The rewrite keeps three things deliberately. Full, prominent credit to
wangyu-/UDPspeeder -- this is a fork and its foundation is honest work, MIT
carried forward. The two READMEs stay 1:1 aligned, English and Chinese
carrying the same structure, section for section, so neither language is a
second-class reader again. And the diagrams are mermaid in the markdown
itself, so they render wherever the README does and version with the text
that explains them.

## What the new front door says

- What this is: a fork of UDPspeeder that became its own tunnel -- the one
  paragraph lineage with the credit link up front, not buried in a footer.
- Why it is fast: the SIMD story elaborated from OPTIMIZATION.md -- the
  vectorized FEC kernels, the per-CPU dispatch tiers (SSSE3, AVX2, NEON,
  and the PowerPC SPE path), what the dispatcher picks at runtime and the
  measured gain per tier -- with a mermaid flowchart of the dispatch.
- Why it is different: the endpoint that follows DNS, the socket marks, the
  platforms and binaries we actually ship.
- VPN over the tunnel is a key goal: an applied family with one backbone,
  the MTU ledger (path MTU x inner VPN -> safe inner MTU and the knob that
  sets it, every number verified by capturing real stacked packets) --
  WireGuard at full MTU with mark coordination, OpenVPN TCP carried on UDP
  (the loss-rescue claim with its double-spend tension left live), the
  stranger scenarios (raw TCP, IPv6 inner, double stacking, the no-VPN
  case), and the anti-loop route exception generalized.
- The applied sections: tuning a lossy link (ratio table, live fifo
  levers, measure-your-own-link), the moving endpoint, what this is not
  (five honest lines), which binary for which CPU, and troubleshooting
  routed to its own guide.
- Quick start both ways: command line and OpenWrt UCI, every applied
  section ending in the two-door pattern (CLI block and UCI stanza side
  by side).
- New mermaid diagrams: the tunnel architecture with the marks drawn on the
  outer packets, the endpoint re-pointing when DNS moves, and the SIMD
  dispatch -- three blocks in the markdown, no image files.
- The evidence posture, in plain words: what we claim, we test; the wire
  proofs described as they run.
- Platform table, privileges table, the feed, the license story.

## Writing charter

Four sources govern the prose and the ink, and every task's verify line
enforces them. Practitioner Voice (Highsmith on martinfowler.com): sections
open with claims, authority comes from consequence, scars are credibility,
tensions are named and left live, compression respects the reader, a carry
phrase closes. Tufte: data-ink maximized, tables as small multiples,
graphics inside the prose flow, every number adjacent to its origin, empty
cells stated as data. Diataxis: every section declares one quadrant and
keeps its register; the README routes what it does not own; blur is the
named failure. The Good Docs Project: status and engage sections present;
an EN-zh terminology table keeps the two READMEs a translation of record.
Personas describe readers inside this host's rooms only; the shipped
documents never name them, and no methodology vocabulary appears in the
artifacts.

## Build sequence

### Inventory the old READMEs against reality {#inventory-the-old-readmes-against-reality}

- verify: every claim in the current READMEs classified as still-true, stale, or fork-unique; the stale list names what the rewrite must replace
- inputs: software/udpspeeder-simd/main/README.md, software/udpspeeder-simd/main/doc/README.zh-cn.md

### Elaborate the SIMD kernels {#elaborate-the-simd-kernels}

- depends: #inventory-the-old-readmes-against-reality
- verify: the section names each kernel family, its vector width, the dispatch tier that selects it, and the measured gain, every number traceable to OPTIMIZATION.md or the bench lane
- inputs: software/udpspeeder-simd/main/OPTIMIZATION.md, software/udpspeeder-simd/main/bench/test_dispatch.cpp, software/udpspeeder-simd/main/bench/arch-matrix.awk

### Write the VPN-over-tunnel family {#write-the-vpn-over-tunnel-family}

- depends: #inventory-the-old-readmes-against-reality
- verify: the MTU ledger's every cell verified by capturing real stacked packets (WireGuard and OpenVPN UDP at 1500 and 1492 paths); the WireGuard recipe runs as written with both marks rules non-conflicting; the OpenVPN TCP transport's refusal is recorded as measured (clarified 2026-11-13: the intended family was OpenVPN over UDP; the plan's original wording asked for a TCP stacking, which the tunnel's nature refuses); the UDP section states the double-spend tension for inner TCP flows without resolving it; doc/vpn-over-the-tunnel.md supersedes the upstream openvpn guide with credit retained
- inputs: software/udpspeeder-simd/main/doc/udpspeeder_openvpn.md, software/udpspeeder-simd/main/bench/throughput.sh

### Write the applied sections {#write-the-applied-sections}

- depends: #inventory-the-old-readmes-against-reality, #write-the-vpn-over-tunnel-family
- verify: each recipe runs as written; every applied section ends in the two-door pattern; tuning table, moving endpoint, what-this-is-not, which-binary sections present in both languages with no untraceable numbers

### Write the OpenWrt section {#write-the-openwrt-section}

- depends: #write-the-applied-sections
- verify: deployment from the release assets only (operator ruling 2026-11-13: no feed door, no upstream claims); the procd service pattern follows OpenWrt's documented interface; every asset name matches the v1.2.2 release; the section is in both languages and routes to doc/openwrt.md; no claim about the feed package or upstream inclusion

### Write the troubleshooting guide {#write-the-troubleshooting-guide}

- depends: #write-the-applied-sections
- verify: every symptom traced to a real incident on record (ratio, MTU blackhole, dscp remarking downstream, admission-refused fatal); symptom-cause-fix form; routed to doc/ and linked from both READMEs

### Write the English README {#write-the-english-readme}

- depends: #elaborate-the-simd-kernels, #write-the-applied-sections, #write-the-openwrt-section
- verify: sections open with claims, each declares one quadrant and keeps its register, the three tensions named and left live, a reader can install, stack a VPN at correct MTU, and answer why-this-over-upstream without leaving the page; the two scars as stories were cut by operator ruling 2026-11-14 ("is crap. drop it") after being read on the page, and both READMEs carry no scars section

### Author the mermaid diagrams {#author-the-mermaid-diagrams}

- depends: #inventory-the-old-readmes-against-reality
- verify: three mermaid blocks render on GitHub -- the architecture with marked outer packets, the DNS re-point, and the SIMD dispatch; no upstream images remain referenced

### Write the Chinese README, one to one {#write-the-chinese-readme-one-to-one}

- depends: #write-the-english-readme, #author-the-mermaid-diagrams
- verify: section-for-section alignment with the English README; the same mermaid blocks; a native reader confirms the register is documentation, not machine translation

### Translate the socket-marks guide {#translate-the-socket-marks-guide}

- depends: #write-the-chinese-readme-one-to-one
- verify: the guide exists in Chinese with the quick-reference table intact and the promise paragraph carrying the same force

### Hold every claim to evidence {#hold-every-claim-to-evidence}

- depends: #write-the-english-readme, #write-the-chinese-readme-one-to-one, #translate-the-socket-marks-guide, #write-the-troubleshooting-guide
- verify: each performance, platform and feature statement in every shipped document traces to a lane, a spec, or a document; the untraceable are removed rather than softened; no persona names or methodology vocabulary appear in any artifact; the EN-zh terminology table covers every term the two READMEs share

### Ship the man page {#ship-the-man-page}

- depends: #hold-every-claim-to-evidence
- verify: the man page is generated from the binary's own --help by a make target (so it cannot drift), renders under mdoc, installs with make install, the version bump to v1.3.0 and the regenerated page share one commit under a matching tag, and the release publishes from the tag
