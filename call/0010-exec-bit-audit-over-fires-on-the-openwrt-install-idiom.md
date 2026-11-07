# The exec-bit audit over-fires on the OpenWrt install idiom

- Status: superseded by call/0011
- Scope: packages, openwrt
- Date: 2026-11-07

## Context and Problem Statement

The template upgrade applied on 2026-11-07 (through ledger entry
[PIN-two-surfaces-two-claims](https://github.com/connollydavid/host-template))
brought this host to the toolchain where `software --check` audits invoked
entry points for the executable bit. On the first full run after
`software --materialize` (a fresh checkout; nothing hand-modified), the audit
reported 514 HAZARDs across two foreign source pins: `packages` (the fork of
the OpenWrt packages feed, master mirroring upstream) and `openwrt` (the
buildroot, consumed upstream).

Every finding is the same shape: a file invoked as `./files/<name>` inside a
package Makefile while recorded 100644. In the OpenWrt feed those invocations
live inside install macros, chiefly `$(INSTALL_BIN)`, which copies the file
into the staging directory and applies the executable mode at copy time. The
source mode is the feed's own deliberate layout; the sources are never
executed in place, so the "exit 126 in a fresh clone" scenario the audit names
cannot arise from this idiom. One further finding of the same audit was real
and was fixed the ordinary way: `bench/dns-live-test.sh` in udpspeeder-simd
documented its own `./` invocation in a usage comment while recorded 100644
(mode committed in the component at `bce0f3c`, re-pinned in the same session).

The audit's printed remedy (staging `git update-index --chmod=+x` per path)
cannot be committed for these two components without diverging the fork from
the upstream feed, and for `openwrt` there is no fork to commit to.

## Decision

- The 514 findings over `packages` and `openwrt` are a confirmed over-fire of
  the shared audit, reported upstream as
  [host-lifecycle issue 45](https://github.com/connollydavid/host-lifecycle/issues/45)
  with the fresh-checkout context and the install-macro mechanism. The project
  that finds an over-fire proposes it to the shared tool; it does not edit the
  corpus to satisfy the gate.
- Interim, until the tool learns the idiom, the audit's own printed remedy is
  applied verbatim on this machine: the staged chmods live in the worktree
  indexes of the two foreign pins, keep their HEADs at the recorded pins, and
  commit nothing. The remedy is local state: `software --materialize` (and
  therefore `bootstrap`) resets it, so a fresh setup must re-apply it. The
  remedy commands are exactly what `software --check` prints per finding; the
  gate re-derives its own instruction list on every run.
- The one genuine finding in this host's own software was fixed in the
  component and re-pinned; it is not part of the interim state.

## Consequences

- `software --check` reads green at the declared toolchain (host-lifecycle
  v0.50.0, pinned in `.env`), and the verify receipt re-verifies.
- The green reading depends on interim local state that a re-materialize
  resets; a future gate run that re-prints the corpus is re-applying the
  staged remedy, not discovering new findings. This entry is the record that
  distinguishes the two.
- When host-lifecycle ships a fix (skipping install-macro invocations, or a
  sanctioned exemption for foreign source pins), this interim state is
  retired: drop the staged chmods, adopt the tool bump through the template
  ledger, and mark this decision superseded by the entry that carries it.
