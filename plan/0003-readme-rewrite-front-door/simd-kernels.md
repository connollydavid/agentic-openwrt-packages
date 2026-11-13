# The SIMD kernels, elaborated

Working material for `#elaborate-the-simd-kernels`. This is the section the
new README absorbs under "why it is fast". Every number below carries its
origin: an OPTIMIZATION.md section or a bench-lane artifact. Vector widths
and dispatch rules are read from the code that implements them (`lib/fec.cpp`,
`packet_cook.cpp`, `xor_spe.S`) and from `bench/arch-map.tsv`, which CI holds
as a check rather than a report.

## The three kernel families

The hot path has three families, and each one dispatches on its own:

| Family | What it computes | Where it runs |
|---|---|---|
| addmul1 | GF(2^8) multiply-accumulate, the inner loop of Reed-Solomon encode and decode | `lib/fec.cpp` |
| xor_tile | XOR of the repeating key and IV patterns over the packet (obscure plus encryption) | `packet_cook.cpp` |
| crc32c | The Castagnoli checksum over the packet body | `crc32c.h`, resolved by `crc32c_resolve` |

## addmul1: the Reed-Solomon inner loop

The scalar original multiplies one byte at a time through a 64 KB lookup
table. The vector paths decompose each byte into low and high nibbles and use
a byte shuffle as a 16-entry parallel table lookup: `PSHUFB` on x86, `TBL` on
ARM, XOR the two partial products. Sixteen bytes per iteration, with a scalar
tail for the remainder. AVX2 widens the same scheme to 256-bit registers;
because `VPSHUFB` operates on two independent 128-bit lanes, the 16-byte
lookup table is broadcast into both (`_mm256_broadcastsi128_si256`), and an
SSE tail covers the 16 to 31 byte remainder.

The x86 dispatch is a three-phase CPUID probe resolved once in `init_fec()`:
OSXSAVE plus XCR0 AVX state plus leaf 7 bit 5 before AVX2 is allowed, the
same OS-support discipline extended to AVX-512BW (which the probe declines
where the OS does not enable opmask and ZMM state). The tier ladder, from
`lib/fec.cpp`:

| Tier | Vector width | Selection | Measured at 1500 B |
|---|---|---|---|
| scalar | 1 B | no SIMD, the base | 1578.8 ns, 0.95 GB/s |
| sse2 | 16 B | CPUID leaf 1, SSE2, when SSSE3 is absent | 913.3 ns, 1.64 GB/s, 1.73x over scalar |
| ssse3 | 16 B | CPUID leaf 1 ECX bit 9 | 161.3 ns, 9.30 GB/s, 9.8x over scalar |
| avx2 | 32 B | three-phase probe | in the ssse3 to avx2 step of the 11.5x whole-path gain |
| avx512bw | 64 B | full OS-support probe | guarded; declined where the OS withholds the state |
| neon | 16 B | build-time, the ARM toolchain's FPU default | the a15 row of the arch map |
| scalar | 1 B | build-time, cores with no vector unit | the a9, mips, riscv64 rows |

The SSE2 tier is the one that makes the ladder safe rather than fast: it has
no byte shuffle, so it multiplies by repeated doubling in the field
(`_mm_add_epi8(x, x)` with a conditional reduction), no tables and no memory
traffic. It exists because x86_64 does not imply SSSE3 (OPTIMIZATION.md #16
tells the story: AMD K8 and K10, and the early 64-bit Intel parts, lack it,
and the first `PSHUFB` there was a SIGILL that killed the tunnel on its first
FEC batch; the crash was found under `qemu64`, the conservative baseline
model, which no developer machine or CI runner had ever matched).

Whole-path numbers, from the microbenchmark summary at 1500 B:

| Path | Before | After | Speedup |
|---|---|---|---|
| addmul1 | 665 ns | 58 ns | 11.5x |
| rs_encode k=10 n=15 | 34,000 ns | 3,100 ns | 11x |
| rs_decode k=10 n=15 | 36,000 ns | 4,500 ns | 8x |

## xor_tile: the cook pipeline

Every packet is cooked: checksummed, obfuscated, and (with a key) encrypted,
all XOR-shaped work. The original walked byte at a time with data-dependent
branches (`if (key[j] == 0) j = 0`), which compilers cannot vectorize. The
vector path pre-expands the repeating key or IV pattern into a tile whose
length is the least common multiple of the pattern length and 16, computes
the key tile once at startup, builds the IV tile per packet on the stack
(at most 496 B), and XORs 16 bytes at a time.

| Tier | Vector width | Selection |
|---|---|---|
| word | one machine word (`sizeof(unsigned long)`) | the generic fallback, MIPS, RISC-V, ARMv7 without NEON |
| sse2 | 16 B | x86 baseline, compile-time |
| avx2 | 32 B | runtime probe with the OSXSAVE and XCR0 YMM check |
| neon | 16 B | build-time, the ARM toolchain default |
| spe | 8 B doubleword | PowerPC e500v2, a build guard (`make SPE=1`) |

The SPE tier is hand-written assembly (`xor_spe.S`) for the e500v2 core
(Freescale P1014, the TP-Link TL-WDR4900 among others), which has no AltiVec.
GCC 9 removed the SPE intrinsics, so the kernel follows the Linux kernel's
own pattern for SPE crypto (`arch/powerpc/crypto/aes-spe-core.S`): a 4x
unrolled `evldd`/`evxor`/`evstdd` main loop at 32 B per iteration, alignment
head and tail loops, and tile buffers padded so an unaligned offset cannot
straddle the end. SPE cannot help addmul1 (byte-level shuffle is absent) or
CRC32C (no hardware CRC on the e500v2), so on PowerPC the gains are the XOR
stage plus the allocator work below.

Measured:

| Path | Before | After | Speedup |
|---|---|---|---|
| XOR-encryption stage alone | 1,826 ns | 131 ns | 14x |
| whole `do_cook` | 3,000 ns | 713 ns | 4.2x |

On PowerPC under
QEMU, `do_cook` at 1500 B stands at 4,090 ns with the SPE stage
(`cook_xor_only` 1,091 ns of it), and RS encode improved 1.5x there from the
decode-buffer preallocation alone.

## crc32c: the checksum

The zlib CRC32 became CRC32C (Castagnoli), which has hardware support worth
taking: `_mm_crc32_u64` under SSE4.2 on x86, `__crc32cb` under ARMv8. The
resolver probes once; without hardware support the software path is a
slicing-by-8 Castagnoli table, itself faster than the zlib CRC32 it replaced
(on PowerPC, 2,609 ns to 1,804 ns at 1500 B, a 1.4x gain from the switch
alone).

## What the tiers choose at runtime, and who checks

On x86 the three ladders resolve at startup by CPUID probe. On the feed
targets the choice is made by the build: the compiler the OpenWrt toolchain
configures decides whether the NEON paths exist in the binary at all, and
`bench/arch-map.tsv` records, for every shipped architecture, the path each
dispatcher must land on when its binary runs under a named QEMU CPU model:

| Row | addmul1 | xor_tile | crc32c |
|---|---|---|---|
| x86_64 | any (pinned by the cpu-dispatch job against named models) | any | any |
| aarch64 | neon | neon | sw |
| armv7-neon (cortex-a15) | neon | neon | sw |
| armv7-scalar (cortex-a9) | scalar | word | sw |
| mips | scalar | word | sw |
| powerpc (e500v2) | scalar | spe | sw |
| riscv64 | scalar | word | sw |

`bench/test_dispatch.cpp` turns each row into a check: under
`EXPECT_DISPATCH_HELD`, an unnamed expectation fails the run, and the chosen
path must equal the named one. The cpu-dispatch job pins x86_64 down the same
way (`qemu64` yields SSE2, `Nehalem` SSSE3, `Haswell` AVX2; AVX-512BW is
declined under qemu-user because the OS-support check is honest). The
two-row ARM pair is deliberate: the a15 row proves the vector paths are
reached, the a9 row proves they stay out of a build for a core with no NEON
unit, both built with the toolchains the feed actually uses.

## The end-to-end claim

All of it composes into the tunnel numbers, measured end to end on CI
runners (1400 B UDP, loopback). The ranges are CI host variance; each
current-to-baseline pair is measured on the same host within one run, and FEC
overhead dropped from about 41% of throughput to about 30%:

| Config | Baseline | Current | Improvement |
|---|---|---|---|
| no-fec | 618-861 Mbps | 942-1517 Mbps | +48-76% |
| fec 20:10 | 364-509 Mbps | 657-1082 Mbps | +81-113% |

## Notes for the README assembly

- The SIGILL story (OPTIMIZATION.md #16) is the scar to tell: the multiply
  was correct on every machine that had SSSE3, and choosing it on a CPU
  without it killed the tunnel. It is also why the dispatch is probed and
  held rather than assumed, which the arch-map table shows.
- The dispatch mermaid block draws the addmul1 ladder with the OS-support
  gates, and the arch-map rows as the leaf labels.
- Numbers to keep adjacent to their origins in the README tables: the 1500 B
  microbenchmarks and the end-to-end ranges, each cited to OPTIMIZATION.md;
  the arch-map rows cited to the bench lane.
- The fork never claims the unmeasured: Android and Raspberry Pi appear
  nowhere in the arch map, so they appear nowhere in the platform table.
