# The three mermaid blocks

Working material for `#author-the-mermaid-diagrams`. The blocks below are the
diagrams the two READMEs carry: the tunnel architecture with the marks drawn
on the outer packets, the endpoint re-point when DNS moves, and the SIMD
dispatch ladder. They are mermaid in the markdown, so they render wherever
the README renders and version with the prose that explains them. No upstream
image remains referenced after the rewrite (the inventory's stale digest,
item seven).

## The tunnel, with the marks on the outer packets

The marks are host-local: they ride the tunnel's own outer packets and change
how those are routed, filtered, or queued. The inner packet is untouched; the
two ends need not agree on any mark.

```mermaid
flowchart LR
    APP["application<br/>UDP traffic"] -->|"inner packet"| C["udpspeeder-simd<br/>client"]
    C -->|"FEC group:<br/>20 original + 10 redundant"| P["outer packets<br/>cooked: crc32c + xor<br/>marked: fwmark / cookie / dscp"]
    P -->|"lossy high-latency link<br/>any 10 of 30 survive: decode"| S["udpspeeder-simd<br/>server"]
    S -->|"decoded inner packet"| T["the service<br/>127.0.0.1:7777"]
```

## The endpoint re-point when DNS moves

The client's `-r` takes a hostname. The lease manager refreshes the record
before its TTL expires and re-points the tunnel when the address changes, so
a moving endpoint never reads as an outage.

```mermaid
sequenceDiagram
    participant C as udpspeeder-simd client
    participant D as DNS resolver
    participant O as old endpoint 203.0.113.7
    participant N as new endpoint 198.51.100.9
    C->>D: resolve tunnel.example.net, before TTL expiry
    D-->>C: 203.0.113.7, TTL 300
    C->>O: outer packets
    Note over D: the record changes
    D-->>C: 198.51.100.9, TTL 300
    C->>N: outer packets, same session
    Note over C: the tunnel re-points without a restart
```

## The SIMD dispatch

On x86 the kernel ladders resolve at startup by CPUID probe; on the feed
targets the build decides. Every leaf below is a row CI holds as a check
under a named QEMU CPU model.

```mermaid
flowchart TD
    A["the FEC inner loop:<br/>GF multiply-accumulate"] --> Q{"x86_64 host"}
    Q -->|"OS enables ZMM state"| AV5["avx512bw, 64 B"]
    Q -->|"OS enables YMM state"| AV2["avx2, 32 B"]
    Q -->|"CPUID leaf 1 ECX bit 9"| SS3["ssse3, 16 B, PSHUFB nibble lookup"]
    Q -->|"SSE2 only"| S2["sse2, 16 B, repeated doubling"]
    Q -->|"no vector unit"| SC["scalar"]
    A --> B{"the build target"}
    B -->|"ARM toolchain with NEON"| NE["neon, 16 B, TBL lookup"]
    B -->|"PowerPC e500v2"| SPE["spe, 8 B, evxor assembly"]
    B -->|"mips, riscv64, armv7 without NEON"| W["word-width xor and scalar multiply"]
```

## Notes for the README assembly

- The blocks carry no upstream images and no image files; the rewrite deletes
  every `/images/` reference the inventory listed.
- Ink discipline: each diagram names its actors and its claim, nothing more;
  the numbers live in the adjacent tables, not inside the boxes.
- The dispatch diagram's leaves are the arch-map rows verbatim, so the
  diagram and the CI check cannot drift apart silently.
