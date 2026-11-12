# PLAN: milestone index

The ordering authority. Milestones are listed here in the order they are worked;
their folders are named `NNNN-slug` (zero-padded, and the number is identity, not a
sort key; see `call/0000`). A milestone is a thin, persona-serving increment.

Worked in this order:

- [0000-openwrt-udpspeeder-simd-package](0000-openwrt-udpspeeder-simd-package/README.md).
  Adds an OpenWrt feed package for udpspeeder-simd that answers the request at
  https://github.com/openwrt/packages/issues/28562 (Ingrid's story).
- [0001-dns-lease-manager](0001-dns-lease-manager/README.md).
  Adds a DNS lease manager to udpspeeder-simd so the client's `-r` takes a hostname,
  resolving it to candidate IPs, refreshing before TTL expiry, and re-pointing the
  tunnel across IP changes and collapse; ships as v1.1.0, the first minor bump
  (Diego's story, Samira's spec-lane obligations).
- [0002-udpspeeder-simd-socket-marks](0002-udpspeeder-simd-socket-marks/README.md).
  Adds `--fwmark`, `--cookie` and `--dscp` socket marks with an honor-or-refuse
  contract, a Windows qWAVE tier, FreeBSD and Windows CI lanes, and the UCI
  wiring for the marks Linux honors (Diego's shaping story, sdanfa's request).
