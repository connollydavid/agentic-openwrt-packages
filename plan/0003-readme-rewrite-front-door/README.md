# README rewrite: the front door for our own software

- Status: planned
- Persona: Diego (primary reader — installs, configures, watches it run);
  Ingrid (reads it for packaging truth); Samira (holds its claims to evidence)
- Serves: every new visitor to the repository, and sdanfa's class of user who
  arrives with one feature in mind
- Scope: the `udpspeeder-simd` component's two READMEs and the marks guide,
  with new mermaid diagrams and an elaborated SIMD section; no code, no release

## Why

The READMEs are still upstream's: their structure, their diagrams, their
story. The software underneath stopped being upstream long ago — the SIMD
kernels, the DNS lease manager that follows a moving endpoint, the socket
marks with their honor-or-refuse contract, four-host CI that reads the
priority byte off the wire, the OpenWrt packages, the renamed binary. A
visitor reading the front door meets wangyu-'s UDPspeeder with footnotes,
not the software they would actually run. The Chinese README compounds it:
a translation of the old English one, one version behind even that.

The rewrite keeps three things deliberately. Full, prominent credit to
wangyu-/UDPspeeder — this is a fork and its foundation is honest work, MIT
carried forward. The two READMEs stay 1:1 aligned, English and Chinese
carrying the same structure, section for section, so neither language is a
second-class reader again. And the diagrams are mermaid in the markdown
itself, so they render wherever the README does and version with the text
that explains them.

## What the new front door says

- What this is: a fork of UDPspeeder that became its own tunnel — the one
  paragraph lineage with the credit link up front, not buried in a footer.
- Why it is fast: the SIMD story elaborated from OPTIMIZATION.md — the
  vectorized FEC kernels, the per-CPU dispatch tiers (SSSE3, AVX2, NEON,
  and the PowerPC SPE path), what the dispatcher picks at runtime and the
  measured gain per tier — with a mermaid flowchart of the dispatch.
- Why it is different: the endpoint that follows DNS, the socket marks, the
  platforms and binaries we actually ship.
- Quick start both ways: command line and OpenWrt UCI, Diego's two doors.
- New mermaid diagrams: the tunnel architecture with the marks drawn on the
  outer packets, the endpoint re-pointing when DNS moves, and the SIMD
  dispatch — three blocks in the markdown, no image files.
- The evidence posture, in plain words: what we claim, we test; the wire
  proofs described as they run.
- Platform table, privileges table, the feed, the license story.

## Build sequence

### Inventory the old READMEs against reality {#inventory-the-old-readmes-against-reality}

- verify: every claim in the current READMEs classified as still-true, stale, or fork-unique; the stale list names what the rewrite must replace
- inputs: README.md, doc/README.zh-cn.md

### Elaborate the SIMD kernels {#elaborate-the-simd-kernels}

- depends: #inventory-the-old-readmes-against-reality
- verify: the section names each kernel family, its vector width, the dispatch tier that selects it, and the measured gain, every number traceable to OPTIMIZATION.md or the bench lane
- inputs: OPTIMIZATION.md, bench/test_dispatch.cpp, bench/arch-matrix.awk

### Write the English README {#write-the-english-readme}

- depends: #elaborate-the-simd-kernels
- verify: a new reader (Diego stand-in) can install, configure with marks, understand why it is fast, and find the answer to "why this over upstream" without leaving the page

### Author the mermaid diagrams {#author-the-mermaid-diagrams}

- depends: #inventory-the-old-readmes-against-reality
- verify: three mermaid blocks render on GitHub — the architecture with marked outer packets, the DNS re-point, and the SIMD dispatch; no upstream images remain referenced

### Write the Chinese README, one to one {#write-the-chinese-readme-one-to-one}

- depends: #write-the-english-readme, #author-the-mermaid-diagrams
- verify: section-for-section alignment with the English README; the same mermaid blocks; a native reader confirms the register is documentation, not machine translation

### Translate the socket-marks guide {#translate-the-socket-marks-guide}

- depends: #write-the-chinese-readme-one-to-one
- verify: the guide exists in Chinese with the quick-reference table intact and the promise paragraph carrying the same force

### Hold every claim to evidence {#hold-every-claim-to-evidence}

- depends: #write-the-english-readme, #write-the-chinese-readme-one-to-one, #translate-the-socket-marks-guide
- verify: each performance, platform and feature statement in all three documents traces to a lane, a spec, or a document; the untraceable are removed rather than softened
