# agentic-openwrt-packages

The governance shell for **UDPspeeder-simd**, a Forward Error Correction UDP tunnel
(C++, forked from UDPspeeder). This repository holds the *thought*: the plans,
decisions, personas, and the operating manual. The software itself, the *action*,
lives beneath it as a bare store with a worktree, kept separate and independently
versioned.

Read [`AGENTS.md`](AGENTS.md) first; it is the operating manual and works literally
(`CLAUDE.md` is a pointer to it). [`STRUCTURE.md`](STRUCTURE.md) is the one-page map.
The process that built this host lives in the
[`host` repository](https://github.com/connollydavid/host).

## Layout

| Room | Holds |
|---|---|
| `cast/` | personas (the Who); examples pending replacement |
| `plan/` | the milestone index |
| `call/` | decisions, in MADR format |
| `software/` | the hosted software, materialized locally (gitignored) |
| `tools/` | the verification tools, referenced submodules |

The software is pinned in [`.host-software`](.host-software) and materialized with
`host-lifecycle software --materialize .` into `software/<component>/<branch>/`
(for udpspeeder-simd that is `software/udpspeeder-simd/main/`).

## Tooling

`host-lifecycle` and `host-lint` drive the mechanical work. A fresh clone reaches a
set-up project with one command (`bootstrap` runs the submodules, the materialize,
the skill links, the hooks, and the completeness gate):

```
./tools/install-tools.sh host-lifecycle
host-lifecycle bootstrap .
```

## License

This governance shell is released into the public domain (Unlicense). The hosted
software, UDPspeeder-simd, carries its own MIT license in its worktree.
