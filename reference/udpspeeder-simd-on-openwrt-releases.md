# Using udpspeeder-simd on an OpenWrt release

The udpspeeder-simd package is submitted to the OpenWrt `packages` feed on the
development branch (master). OpenWrt policy is that release branches
(`openwrt-XX.YY`) take only security and bug fixes, not new packages, so
udpspeeder-simd is **not** backported to the release feeds. A developer or power
user on any current release can self-apply it with either route below.

Both routes reuse the package Makefile from the fork, which pins the source to a
fixed commit, so the build is reproducible on any release that has the shared
libraries the package depends on (`libstdcpp`, `librt`, `libatomic`), which every
current release provides.

## Route 1: build with the release SDK

The SDK is the smallest option and needs no full checkout of the buildroot. Pick
the release and the target that match the router, then build the package and copy
the result to the device.

```sh
REL=24.10.0
TARGET=ath79/generic            # your router's target/subtarget

wget "https://downloads.openwrt.org/releases/$REL/targets/$TARGET/openwrt-sdk-"*.tar.zst
tar --zstd -xf openwrt-sdk-*.tar.zst
cd openwrt-sdk-*

# Add udpspeeder-simd as a custom feed, from the fork's PR branch:
echo "src-git udpspeedersimd https://github.com/connollydavid/packages.git;udpspeeder-simd" >> feeds.conf.default
./scripts/feeds update udpspeedersimd
./scripts/feeds install udpspeeder-simd

make defconfig
make package/udpspeeder-simd/compile V=s
# The package lands in bin/packages/<arch>/udpspeedersimd/
```

Copy the resulting package to the router and install it with the release's package
manager: `opkg install ./udpspeeder-simd_*.ipk` where the release uses opkg, or
`apk add ./udpspeeder-simd-*.apk` where it ships apk.

## Route 2: add the feed to a full buildroot

A user who already builds firmware from the buildroot adds the same custom feed,
selects the package in `menuconfig`, and builds it into the image.

```sh
# In your OpenWrt buildroot checked out on the release branch:
echo "src-git udpspeedersimd https://github.com/connollydavid/packages.git;udpspeeder-simd" >> feeds.conf.default
./scripts/feeds update udpspeedersimd
./scripts/feeds install udpspeeder-simd

make menuconfig                 # Network -> udpspeeder-simd, set to <M> or <*>
make package/udpspeeder-simd/compile V=s
```

## Notes

- The package installs at `/usr/bin/udpspeeder-simd` with its own config and init
  script, so it coexists with the stock `udpspeeder` package. Neither replaces the
  other.
- To pin a specific version, edit `PKG_SOURCE_VERSION` in the package Makefile to
  the commit you want, and refresh `PKG_MIRROR_HASH`.
- Once the master PR merges, the package is available from the development feed
  directly, and this custom-feed step is only needed for a release that predates
  the merge.
