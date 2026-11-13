# The applied sections

Working material for `#write-the-applied-sections`: four sections, each in
English and Chinese in 1:1 alignment, each configuration-bearing section
ending in the two-door pattern (the command line beside the OpenWrt UCI
stanza, citing the package's real option names). Recipes are verified live by
`bench/recipes-check.sh` (five claims, five passes); numbers carry their
origins.

---

## Tuning a lossy link (EN)

Start from measurement, not folklore: run the tunnel with `--report 10` and
read the loss it reports before choosing a ratio. The FEC arithmetic then
tells you what a ratio buys: with `x:y`, any `y` of the `x+y` packets in a
group can be lost and the group still decodes, at a bandwidth cost of
`(x+y)/x`.

| ratio | bandwidth | survives per-group loss | shape |
|---|---|---|---|
| `-f4:2` | 1.5x | up to 1/3 | small groups, quick flush |
| `-f20:10` | 1.5x | up to 1/3 | the shipped default, smoother under load |
| `-f1:1` | 2x | up to 1/2 | per-packet doubling, best for games |
| `-f1:3` | 4x | up to 3/4 | rescue mode for very bad links |

(Survivable fractions are Reed-Solomon arithmetic: y erasures of x+y are
always recoverable. Group shape effects are the options document's: group
size x, queue flush at `--timeout`, default 8 ms.)

Burst loss wants `-i` (spread each group over an interval), steady loss wants
a higher ratio, and latency-sensitive traffic wants small groups. The
tunnel's compute cost is not the constraint: with fec 20:10 the optimized
build runs 657-1082 Mbps end to end (OPTIMIZATION.md), so the link, not the
program, gives out first.

Everything above is live-tunable: the fifo takes `fec`, `timeout` and
`queue-len` from a running instance (verified: `bench/recipes-check.sh`,
section A), so tuning is a matter of watching `--report` and echoing a new
ratio.

The two doors:

```bash
# command line: watch, then change under load
udpspeeder-simd -c -l127.0.0.1:3333 -r<server>:4096 -f20:10 -k "passwd" \
  --fifo /tmp/fifo --report 10
echo "fec 4:2" > /tmp/fifo      # retune without restarting
```

```
# OpenWrt UCI (/etc/config/udpspeeder-simd)
config udpspeeder-simd 'tunnel1'
	option enabled '1'
	option server '0'
	option local '127.0.0.1:3333'
	option remote '<server>:4096'
	option fec '4:2'
	option timeout '8'
	option report '10'
	option fifo '/tmp/udpspeeder-fifo'
	option key 'passwd'
```

## 调优一条高丢包链路 (zh)

从测量出发，而不是从传闻出发：先带 `--report 10` 跑起来，读它报告的丢包率，再选冗余比。FEC 的算术告诉你每个比值换来什么：以 `x:y` 为例，一组 `x+y` 个包里任意丢 `y` 个都能恢复，代价是带宽变为 `(x+y)/x` 倍。

| 冗余比 | 带宽 | 组内可承受丢包 | 形态 |
|---|---|---|---|
| `-f4:2` | 1.5 倍 | 至多 1/3 | 小组，快速成组 |
| `-f20:10` | 1.5 倍 | 至多 1/3 | 默认值，负载下更平滑 |
| `-f1:1` | 2 倍 | 至多 1/2 | 逐包加倍，适合游戏 |
| `-f1:3` | 4 倍 | 至多 3/4 | 极差链路的抢救模式 |

（可承受比例是 Reed-Solomon 的算术性质：x+y 中丢 y 个必可恢复。组形态的影响见选项说明：组大小 x，队列到 `--timeout` 便发送，默认 8 毫秒。）

突发丢包加 `-i`（把每组在一个时间窗内摊开发送）；持续丢包提高冗余比；延迟敏感的流量用小组。计算力不是瓶颈：fec 20:10 下优化构建的端到端吞吐为 657-1082 Mbps（见 OPTIMIZATION.md），先到极限的是链路，不是程序。

以上参数全部可以在线调整：运行中的实例通过 fifo 接受 `fec`、`timeout`、`queue-len`（已验证：`bench/recipes-check.sh` A 节），调优就是看着 `--report` 再回显一个新比值。

两扇门：

```bash
# 命令行：先观察，再在运行中调整
udpspeeder-simd -c -l127.0.0.1:3333 -r<server>:4096 -f20:10 -k "passwd" \
  --fifo /tmp/fifo --report 10
echo "fec 4:2" > /tmp/fifo      # 不重启换参
```

```
# OpenWrt UCI（/etc/config/udpspeeder-simd）
config udpspeeder-simd 'tunnel1'
	option enabled '1'
	option server '0'
	option local '127.0.0.1:3333'
	option remote '<server>:4096'
	option fec '4:2'
	option timeout '8'
	option report '10'
	option fifo '/tmp/udpspeeder-fifo'
	option key 'passwd'
```

---

## The moving endpoint (EN)

Give the client a hostname and it follows the address: the lease manager
resolves `-r` names, refreshes before the record's TTL expires, and re-points
the tunnel when the answer changes, without a restart. A moving endpoint (a
residential IP that changes, a failover between two servers) stops reading as
an outage.

The verification is deliberately brutal (`bench/recipes-check.sh`, section
B): two servers on two addresses, traffic through the first, then the DNS
answer flips and the first server dies; the same client process re-points and
passes traffic again. The refresh discipline is the DNS lease manager's
specification (`dns_lease_mgr.allium`, held by the component's CI).

The two doors:

```bash
# command line: the hostname is the whole change
udpspeeder-simd -c -l127.0.0.1:3333 -rmytunnel.example.net:4096 \
  -f20:10 -k "passwd"
```

```
# OpenWrt UCI: the remote takes the hostname the same way
config udpspeeder-simd 'tunnel1'
	option enabled '1'
	option server '0'
	option local '127.0.0.1:3333'
	option remote 'mytunnel.example.net:4096'
	option fec '20:10'
	option key 'passwd'
```

## 移动的对端 (zh)

给客户端一个主机名，它就会跟着地址走：租约管理器解析 `-r` 里的名字，在 TTL 到期前刷新，应答变化时把隧道指向新地址，全程无需重启。会动的对端（会变的家宽地址、两台服务器间的切换）从此不再表现为断线。

验证刻意做到苛刻（`bench/recipes-check.sh` B 节）：两台服务器两个地址，流量先走第一台，然后 DNS 应答翻转、第一台被杀；同一个客户端进程重新指向并通过了流量。刷新纪律由 DNS 租约管理器的规格约束（`dns_lease_mgr.allium`，组件 CI 持有）。

两扇门：

```bash
# 命令行：改的就是一个主机名
udpspeeder-simd -c -l127.0.0.1:3333 -rmytunnel.example.net:4096 \
  -f20:10 -k "passwd"
```

```
# OpenWrt UCI：remote 同样接受主机名
config udpspeeder-simd 'tunnel1'
	option enabled '1'
	option server '0'
	option local '127.0.0.1:3333'
	option remote 'mytunnel.example.net:4096'
	option fec '20:10'
	option key 'passwd'
```

---

## What this is not (EN)

Five honest lines, so nobody arrives by mistake:

1. Not a TCP tunnel: it carries UDP datagrams; TCP traffic rides a VPN
   stacked on top (the VPN-over-the-tunnel guide).
2. Not magic against congestion: FEC repairs loss; it cannot create
   bandwidth, and congestion loss is better left to TCP's own backoff.
3. Not strong encryption: `-k` is an XOR obfuscation with random padding,
   not a cipher; confidentiality is the stacked VPN's job.
4. Not a VPN by itself: it forwards one UDP service; the VPN guide is where
   whole-network access comes from.
5. Not a WAN optimizer: it is a lossy-link tool; on a clean link it only
   adds redundancy.

The two doors are the manual itself:

```bash
udpspeeder-simd -h        # every option, from the binary
```

```
# OpenWrt: the package's config is the documented surface
# /etc/config/udpspeeder-simd (uci show udpspeeder-simd)
```

## 它不是什么 (zh)

五行实话，免得有人误入：

1. 不是 TCP 隧道：它搬运 UDP 数据报；TCP 流量要靠叠在上面的 VPN（见 VPN over the tunnel 指南）。
2. 不是拥塞的解药：FEC 修复丢包，不能凭空造带宽；拥塞丢包交给 TCP 自己的退避更合适。
3. 不是强加密：`-k` 是带随机填充的异或混淆，不是密码学加密；保密性由叠加的 VPN 负责。
4. 本身不是 VPN：它转发一个 UDP 服务；整网接入请看 VPN 指南。
5. 不是广域网优化器：它是丢包链路的工具；干净的链路上它只增加冗余。

两扇门就是手册本身：

```bash
udpspeeder-simd -h        # 每个选项，来自二进制本身
```

```
# OpenWrt：软件包的配置文件即文档化的接口
# /etc/config/udpspeeder-simd（uci show udpspeeder-simd）
```

---

## Which binary for which machine (EN)

The release ships ten assets; the build matrix behind them is
`bench/arch-map.tsv`, the same table CI holds as a check. Pick by the target
CPU:

| asset | machine | example |
|---|---|---|
| `udpspeeder-simd.x86_64` | any x86_64 Linux, old or new | servers, desktops, Atom |
| `udpspeeder-simd.aarch64` | 64-bit ARM | most modern routers, SBCs |
| `udpspeeder-simd.armv7-neon` | 32-bit ARM with NEON | cortex-a15-class targets |
| `udpspeeder-simd.armv7-scalar` | 32-bit ARM without NEON | mvebu cortex-a9 targets |
| `udpspeeder-simd.mips` | big-endian MIPS | ath79-class routers |
| `udpspeeder-simd.powerpc` | PowerPC e500v2 | TL-WDR4900 class |
| `udpspeeder-simd.riscv64` | 64-bit RISC-V | sifiveu targets |
| `udpspeeder-simd.x86_64.exe` | Windows x86_64 | |
| `udpspeeder-simd.aarch64.exe` | Windows on ARM | |
| `udpspeeder-simd` | macOS, both Intel and Apple silicon | one universal binary |

The x86_64 binary runs on CPUs as old as the first K8: the dispatcher probes
before it uses SSSE3 and falls back to SSE2 and scalar (the SIMD section
tells the SIGILL story behind that). On OpenWrt, the package resolves the
right build through the feed.

The two doors:

```bash
# command line: download from the release, chmod, run
curl -LO https://github.com/connollydavid/UDPspeeder-simd/releases/download/v1.2.2/udpspeeder-simd.x86_64
chmod +x udpspeeder-simd.x86_64 && ./udpspeeder-simd.x86_64 -h
```

```
# OpenWrt: the feed package picks the arch itself
opkg update && opkg install udpspeeder-simd
```

## 哪台机器用哪个二进制 (zh)

发布共十件资产；它们背后的构建矩阵是 `bench/arch-map.tsv`，与 CI 检查用的是同一张表。按目标 CPU 选择：

| 资产 | 机器 | 例子 |
|---|---|---|
| `udpspeeder-simd.x86_64` | 任意 x86_64 Linux，新旧皆宜 | 服务器、桌面、Atom |
| `udpspeeder-simd.aarch64` | 64 位 ARM | 多数现代路由器、开发板 |
| `udpspeeder-simd.armv7-neon` | 带 NEON 的 32 位 ARM | cortex-a15 级 |
| `udpspeeder-simd.armv7-scalar` | 无 NEON 的 32 位 ARM | mvebu cortex-a9 级 |
| `udpspeeder-simd.mips` | 大端 MIPS | ath79 级路由器 |
| `udpspeeder-simd.powerpc` | PowerPC e500v2 | TL-WDR4900 一类 |
| `udpspeeder-simd.riscv64` | 64 位 RISC-V | sifiveu 目标 |
| `udpspeeder-simd.x86_64.exe` | Windows x86_64 | |
| `udpspeeder-simd.aarch64.exe` | Windows on ARM | |
| `udpspeeder-simd` | macOS，Intel 与 Apple 芯片同件 | 单一通用二进制 |

x86_64 二进制在最早的 K8 上也能跑：调度器先探测再使用 SSSE3，不满足时退到 SSE2 与标量路径（SIMD 一节讲了这背后的 SIGILL 故事）。在 OpenWrt 上，软件包会通过 feed 自动解析正确的构建。

两扇门：

```bash
# 命令行：从发布页下载、赋权、运行
curl -LO https://github.com/connollydavid/UDPspeeder-simd/releases/download/v1.2.2/udpspeeder-simd.x86_64
chmod +x udpspeeder-simd.x86_64 && ./udpspeeder-simd.x86_64 -h
```

```
# OpenWrt：feed 软件包自己选架构
opkg update && opkg install udpspeeder-simd
```
