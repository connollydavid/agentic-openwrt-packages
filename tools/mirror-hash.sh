#!/usr/bin/env bash
# Recompute an OpenWrt PKG_MIRROR_HASH by replaying include/download.mk's
# git-method src/tarball path: clone, check out the tag, generate the formal
# git archive (apply .gitattributes rules, core.abbrev 8), extract it to a
# directory named <name>-<version>, repack with dl_tar_pack's normalized tar
# (--numeric-owner --owner=0 --group=0 --mode=a-s --sort=name, mtime at the
# commit time) and pack with zstd -T0 --ultra -20, then print the sha256.
# Regression-tested against the v1.0.0 and v1.1.0 hashes already shipped.
#
# usage: mirror-hash.sh <repo-url> <tag> <pkg-name> [pkg-version]
set -euo pipefail
if [ $# -lt 3 ]; then
    echo "usage: $0 <repo-url> <tag> <pkg-name> [pkg-version]" >&2
    exit 2
fi
url=$1; tag=$2; name=$3; ver=${4:-${tag#v}}
subdir="$name-$ver"
command -v zstd >/dev/null || { echo "mirror-hash: zstd is required" >&2; exit 1; }
dir=$(mktemp -d /tmp/opencode/mirror-hash.XXXXXX)
trap 'rm -rf "$dir"' EXIT
git clone -q "$url" "$dir/src"
git -C "$dir/src" checkout -q "$tag"
git -C "$dir/src" config core.abbrev 8
git -C "$dir/src" archive --format=tar HEAD --output="$dir/src.tar.git"
mkdir -p "$dir/dl/$subdir"
tar -C "$dir/dl/$subdir" -xf "$dir/src.tar.git"
mt=$(git -C "$dir/src" log -1 --no-show-signature --format='@%ct')
(cd "$dir/dl" && tar --numeric-owner --owner=0 --group=0 --mode=a-s --sort=name --mtime="$mt" -c "$subdir") |
    zstd -T0 --ultra -20 -q -c > "$dir/$subdir.tar.zst"
sha256sum "$dir/$subdir.tar.zst" | cut -d' ' -f1
