# DNS lease manager for udpspeeder-simd (v1.1.0)

- Status: planned
- Persona: Diego (router administrator); Samira cross-cuts (spec lanes)
- Serves: Diego points the client at a hostname endpoint and the tunnel keeps itself
  alive across IP changes, TTL expiry, and tunnel collapse, without him watching
- Scope: the `udpspeeder-simd` component
- Decisions: [`call/0008`](../../call/0008-udpspeeder-simd-versioning-and-releases.md)
  (versioning and release policy), [`call/0009`](../../call/0009-dns-lease-manager-cxx-single-header.md)
  (the C++-compatible single header)

## Why

The client's `-r` option requires an IP literal today: `address_t::from_str`
(`common.cpp`) splits `host:port` and demands `inet_pton` succeed, so a hostname calls
`myexit(-1)`. Diego's gateway points at a server endpoint he controls on the far
side; when that endpoint moves (dynamic DNS, provider IP churn), he must find the new
address and hand-edit his configuration. A tunnel meant to be an appliance he does
not babysit should follow the endpoint itself.

This milestone adds a DNS lease manager: a single-header, allocation-free,
nonblocking, TTL-aware DNS Locator-Hint Cache. The client resolves `-r hostname:port`
to candidate IPs, leases them for an effective TTL, refreshes before expiry, and
re-points the tunnel when the resolved IP changes. It treats DNS as an untrusted,
mutable locator-hint source (the tunnel test the candidates via the data plane), not
as a trust anchor. This is the first minor version bump; every release before it
was a patch (`v1.0.6` was the last).

The OpenWrt feed package is out of scope here; the fork release is a prerequisite
for a later package bump.

## Design decisions

- The header is written as valid C++11 (`static inline` throughout) rather than
  strict C11, because the fork builds C++-only and the negative constraints the spec
  imposes (no allocation, `mem*` only, no OS resolver, no threads/atomics/signals,
  no recursion/`longjmp`, no float, no unaligned access, no global mutable state, no
  `stdio`) carry over unchanged. See `call/0009`.
- The state machine adds a `STALE` state to the spec's seven: on a failed refresh the
  last-known candidates stay servable until `stale_max_ms` elapses (default 1 hour;
  `0` means serve stale indefinitely). This is the keep-last-known-IP policy, made
  explicit, observable, and TLC-testable.
- TCP fallback on truncation (TC=1) is included, per RFC 1035 and the imported spec:
  the header gains UDP-pending / TCP-connecting / TCP-receiving transport states and
  a 4096-byte TCP receive buffer.
- Client mode only. In server mode the `-r` value names the client endpoint and stays
  IP-only; a hostname there is rejected at parse time with a clear error.
- Verification carries both spec lanes: a `.allium` requirements spec (allium-cli
  check/analyse/plan in the fork CI, obligations discharged by tests) and a `.tla`
  state-machine/timing spec (TLC model check in the fork CI). Specs live with the
  software, per the methodology.
- Release mechanics follow the house rule: the tag is the release; the banner
  `PROGRAM_VERSION` and the tag must agree; the fork CI publishes the per-architecture
  binaries; the host re-pins `.host-software` and records the release receipt.
  Versioning policy is recorded in `call/0008`.

## Build sequence

### Author the DNS lease manager header {#dns-header}

- verify: attested operator

### Author the allium requirements spec and wire its lane {#allium-spec}

- depends: #dns-header
- verify: attested operator

### Author the tla state-machine spec and wire TLC {#tla-spec}

- depends: #dns-header
- verify: attested operator

### Integrate the client {#integrate}

- depends: #dns-header
- verify: attested operator

### Discharge the spec obligations with tests {#tests}

- depends: #allium-spec, #tla-spec, #integrate
- verify: attested operator

### Bump to v1.1.0 and release {#release}

- depends: #tests
- verify: attested operator

### Re-pin the host and record the release {#repin}

- depends: #release
- verify: attested operator