# The OpenWrt section (README stub)

Working material for `#write-the-openwrt-section`: the lean section both
READMEs carry, routing to the full guide. Per the operator ruling of
2026-11-13 it documents deployment from the release assets only.

## EN

### Running on OpenWrt

The release binaries are built with the OpenWrt target toolchains and run on
a stock router: static, about 4.2 MB, no kernel modules, with a receive path
that falls back where the kernel lacks io_uring. Copy the asset for your
target (the which-binary table maps them), and the guide turns it into an
appliance: a procd service that starts at boot, restarts on exit, and reads
`/etc/config/udpspeeder-simd`, so every UCI stanza in this documentation
works verbatim; `uci commit` applies changes, `logread` shows the loss
report, and one line in `/etc/sysupgrade.conf` carries the binary across
firmware upgrades. The whole story, with the init script ready to paste:
[doc/openwrt.md](doc/openwrt.md).

## zh

### 在 OpenWrt 上运行

发布二进制由 OpenWrt 目标工具链构建，在原厂路由器上直接可用：静态链接，约 4.2 MB，无需内核模块；内核缺少 io_uring 时收包路径自动回退。按目标机型选好资产（见哪台机器用哪个二进制一节的对照表），再由指南把它变成一个设备级服务：procd 守护开机自启、退出即重启，并读取 /etc/config/udpspeeder-simd，因此本文档中所有 UCI 配置段均可原样使用；uci commit 即时生效，logread 查看丢包报告，/etc/sysupgrade.conf 加一行即可让二进制随固件升级保留。完整过程与可直接粘贴的 init 脚本见 [doc/openwrt.md](doc/openwrt.md)。
