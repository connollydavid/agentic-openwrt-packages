# The old READMEs, classified against reality

This is the inventory for the task `#inventory-the-old-readmes-against-reality`.
It walks every claim in `README.md` and `doc/README.zh-cn.md` at `v1.2.2`
(`d1e1ee9`) and classifies each as **still-true** (the rewrite carries the
substance, reworded), **stale** (the rewrite must replace it), or **fork-unique**
(fork-era material that is accurate and stays, integrated rather than
rewritten away). The stale digest at the end is the replacement worklist the
later tasks consume.

Reality it classifies against: the software is `udpspeeder-simd` v1.2.2, a fork
of wangyu-'s UDPspeeder with SIMD FEC kernels and per-CPU dispatch, a DNS lease
manager, socket marks (`--fwmark`, `--cookie`, `--dscp`) with an
honor-or-refuse contract, four-host CI that reads the priority byte off the
wire, an OpenWrt feed package, and ten release assets covering seven Linux
arches, both Windows worlds, and one universal macOS binary.

## English README (`README.md`, 185 lines)

| Lines | Claim | Class | Note |
|---|---|---|---|
| 1 | Title: `UDPspeeder` | stale | The software's name is `udpspeeder-simd`; the fork lineage with credit belongs in the first screen |
| 3 | Tagline: a tunnel that improves a high-latency lossy link with FEC | still-true | The one-sentence essence carries |
| 5-6 | UDP alone; UDP-based VPN stacks any traffic; OpenVPN/L2TP/ShadowVPN confirmed | mixed | Mechanism still-true; the confirmed list is upstream-era. The fork's verified family (WireGuard, OpenVPN UDP, OpenVPN TCP) replaces it |
| 8, 12 | Architecture images `udpspeeder.PNG`, `udpspeeder+openvpn3.PNG` | stale | Upstream images, upstream story; three mermaid blocks replace them |
| 14 | Under 0.01% loss at 1.5x traffic; better TCP latency and single-thread speed | mixed | The loss figure is FEC arithmetic at `-f20:10` (still-true as math); the efficacy *presentation* cites no fork measurement and must re-anchor to OPTIMIZATION.md, the bench lane, or stated arithmetic |
| 16 | Wiki link as the primary "more info" pointer | stale | The fork's `doc/` owns the applied material; upstream wiki becomes credited further reading |
| 18 | 简体中文 link | still-true | The 1:1 pairing stays |
| 20-27 | Efficacy screenshots (ping, scp) | stale | 2018 measurements of upstream's binary; not evidence for this software |
| 29-32 | Platforms: Linux (Android, OpenWRT, RPi); Windows/macOS via a 7.5 MB VM image | stale | Ten assets on four hosts replace this; the VM suggestion is obsolete next to native `.exe` and universal mac binaries. Android and RPi are untested by the fork and must not be claimed |
| 34-52 | FEC mechanism, Reed-Solomon, textbook quotes, `fec.PNG`, `rs.png`, Wikipedia | mixed | Substance still-true (RS FEC is the mechanism); the textbook block quote and upstream images go, replaced by the fork's own telling plus the SIMD elaboration |
| 54-57 | Installing: download from upstream releases | stale | Releases are this fork's, v1.2.2, ten assets |
| 59-70 | Running example (server and client lines) | still-true | Correct shape, and the binary name is already the fork's |
| 72-77 | Note: `-f20:10` meaning; `-k` XOR | still-true | |
| 79-81 | "Improves all traffic" section pointing at the upstream wiki OpenVPN guide | stale | `doc/vpn-over-the-tunnel.md` supersedes the upstream guide and the fork's imported copy `doc/udpspeeder_openvpn.md`, with credit retained |
| 85-139 | Full options block | mixed | Banner is stale (`v1.0.6`, git `3e248b414c`, build date Aug 5 2018); the `repository:`/`based on:` lines are fork-unique; the three marks options are fork-unique; every other option line is still-true and matches the real binary. Regenerate the whole block from the v1.2.2 `--help` output |
| 140-148 | `--fifo` section and command examples | still-true | |
| 151-170 | Socket marks section | fork-unique | Accurate (plan/0002), links `doc/socket-marks.md`; stays, and the architecture diagram draws the marks on the outer packets |
| 172-175 | Wiki section | stale | Same as line 16 |
| 177-185 | Related repos: tinyfecVPN, udp2raw | still-true | Upstream-ecosystem pointers; keep with credit framing |

## Chinese README (`doc/README.zh-cn.md`, 240 lines)

| Lines | Claim | Class | Note |
|---|---|---|---|
| 1-2 | Title `UDPspeeder`, banner image | stale | Same as the English title |
| 4 | Intro: essence, the 1.5x/0.01% arithmetic, comparison against kcptun/finalspeed/BBR | mixed | Essence and arithmetic still-true; the 2017 competitor comparison is stale positioning |
| 6 | Personal anecdote: months of use, Brawl Stars, Mobile Legends, first-person 我 | stale | Upstream author's voice and story; the rewrite speaks from this fork's evidence |
| 8 | v1/v2 version talk; link to `README.zh-cn.v1.md` | stale | Upstream lineage; the archive doc stays in the tree, out of the front door |
| 10-12 | Stacking diagram `Capture2.PNG`; confirmed VPNs incl. a censored `$\*\*\*VPN$` | stale | Replaced by the mermaid architecture and the fork's verified family |
| 14-16 | English link; wiki link | mixed | Language pairing still-true; wiki pointer stale-as-primary |
| 18-24 | tinyfecVPN 提示 | still-true | Pointer carries |
| 27-30 | 效果 screenshots | stale | Upstream measurements |
| 33-38 | 原理简介: FEC, Reed-Solomon, `fec.PNG` | mixed | Substance still-true; image goes |
| 40-51 | 其他功能: obscuring, `-i` spreading, `-j` jitter, `--report`, loss/latency/jitter simulation, multiple clients and connections | still-true | All present in the binary; keep, reworded |
| 53-55 | 关键词 keyword block | stale | 2017-era search keywords |
| 59-67 | 环境要求: Linux hosts; prebuilt `amd64`/`x86`/`arm`/`mips_be`/`mips_le`; Windows/macOS VM image (with its root password); Android via terminal | stale | Old asset names, the VM image with its password, and untested Android claims all go; the ten-asset four-host table replaces |
| 69-72 | 安装: upstream releases | stale | Fork releases |
| 74-84 | 运行 example with `--mode 0` | still-true | |
| 86-94 | 备注: `-f20:10`, option spacing rules, `-k`, mode 0 recommendation, game parameters via wiki | mixed | The first three still-true; the wiki-as-primary routing is stale |
| 96-102 | udp2raw 提示 | still-true | Pointer carries |
| 106-160 | 命令选项 block | mixed | Same verdict as the English block: stale banner, fork-unique marks lines (already in Chinese), still-true options; regenerate from v1.2.2 help |
| 161-215 | Per-option explanations (`-f` through `--disable-obscure`) | still-true | Accurate and better written than the English side; the rewrite's advanced section keeps this register in both languages |
| 216-222 | 推荐参数, 使用经验 wiki links | stale-as-primary | The tuning section owns this; the wiki links stay as credited further reading |
| 224-227 | 编译教程 routed to udp2raw's build guide | stale | The fork builds with `make` or CMake; its build story is its own |
| 229-233 | 套接字标记 section | fork-unique | Accurate Chinese summary of the marks; stays |
| 235-239 | wiki section | stale-as-primary | |

## The EN-zh divergence

The Chinese file carries strictly more upstream residue than the English one:
the personal anecdote, the v1/v2 version talk, the keyword block, the VM image
instructions with password, and the old architecture names all survive only on
the Chinese side. That is the concrete content of "one version behind": the
fork-era updates (binary rename, marks sections) landed on both, but nothing
ever pruned the Chinese side's older strata. The 1:1 rewrite closes this by
construction: one structure, two languages, same mermaid blocks.

## The stale digest: what the rewrite must replace

1. **Identity.** The name and title story on both files, replaced by the fork's
   own front door with the credit link up front.
2. **Platform and install truth.** Upstream release URL, the VM image (and its
   root password), old arch names, Android and RPi claims. Replaced by the
   ten-asset four-host table, the privileges table, and the feed.
3. **Efficacy presentation.** Upstream's 2018 screenshots and unanchored
   numbers. Replaced by claims traced to OPTIMIZATION.md, the bench lane, or
   stated FEC arithmetic.
4. **The VPN stacking story.** Upstream's confirmed-VPN list and wiki guide
   pointer. Replaced by the fork's VPN-over-tunnel family with the MTU ledger.
5. **The options banner.** The v1.0.6 block regenerated from the real v1.2.2
   help output.
6. **Upstream's voice.** The personal anecdote, v1/v2 version talk, keyword
   block, competitor comparison.
7. **Every upstream image reference.** Three mermaid blocks replace them.
8. **The wiki as primary pointer.** The fork's `doc/` owns applied material;
   the upstream wiki remains as credited further reading.

What carries: the FEC/Reed-Solomon substance, the quick-start shape, all option
semantics and the per-option explanations, the fifo section, both marks
sections, the related-repo pointers, and the language pairing. What is already
ours: the marks options and sections, the renamed binary in examples, the
repository credit lines in the help block, and `doc/socket-marks.md`.
