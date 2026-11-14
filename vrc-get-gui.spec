# SPDX-License-Identifier: MPL-2.0
#
# COPR packaging for ALCOM, the Tauri based graphical client shipped in the
# vrc-get repository as vrc-get-gui.
#
# License note: the gui-v1.1.10 release tarball packaged here is licensed
# under MIT.  Upstream switched to MPL-2.0 on master after that release; when
# packaging a newer release, update the License tag accordingly.
#
# Sources are fetched from the upstream release tag archives:
#   https://github.com/vrc-get/vrc-get/archive/refs/tags/gui-v1.1.10.tar.gz

%global debug_package %{nil}
%global cargo_target_dir %{_builddir}/target-%{name}

Name:           vrc-get-gui
Version:        1.1.10
Release:        1%{?dist}
Summary:        ALCOM - Alternative Creator Companion

License:        MIT
URL:            https://vrc-get.anatawa12.com/alcom/
Source0:        https://github.com/vrc-get/vrc-get/archive/refs/tags/gui-v%{version}.tar.gz#/vrc-get-gui-v%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  nodejs
BuildRequires:  npm
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(webkit2gtk-4.1)
BuildRequires:  pkgconfig(javascriptcoregtk-4.1)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  desktop-file-utils

Requires:       hicolor-icon-theme
Provides:       alcom = %{version}-%{release}

%description
ALCOM (vrc-get-gui) is a fast, open-source alternative to the VRChat Creator
Companion (VCC), built with Rust and Tauri.  It provides a graphical interface
for managing VPM packages, Unity projects and package repositories.

%prep
%setup -q -n vrc-get-gui-v%{version}

%build
export CARGO_HOME=%{_builddir}/cargo-home
export CARGO_TARGET_DIR=%{cargo_target_dir}
export CCACHE_DIR=%{_builddir}/ccache
export npm_config_cache=%{_builddir}/npm-cache
# Tauri/Rust builds are memory hungry; keep the parallelism suitable for the
# smaller COPR builders as well.
export CARGO_BUILD_JOBS=4
export CARGO_NET_RETRY=10

cargo run --profile xtask -p xtask -- build-alcom --release --no-self-updater \
    --updater-instruction-message 'en=Update ALCOM with: sudo dnf upgrade vrc-get-gui'

%install
export CARGO_HOME=%{_builddir}/cargo-home
export CARGO_TARGET_DIR=%{cargo_target_dir}
cargo run --profile xtask -p xtask -- bundle-alcom --release \
    --bundles buildroot --buildroot=%{buildroot}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/alcom.desktop

%files
%license LICENSE
%doc README.md CHANGELOG-gui.md
%{_bindir}/alcom
%{_datadir}/applications/alcom.desktop
%{_datadir}/icons/hicolor/*/apps/alcom.png

%changelog
* Sat Nov 14 2026 ringlo <ringlo@users.noreply.github.com> - 1.1.10-1
- Initial COPR package for Fedora
