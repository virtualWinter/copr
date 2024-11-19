# RPM Spec file for modrinth-app
Name:           modrinth-app
Version:        0.8.9
Release:        2%{?dist}

Summary:        An unique, open source launcher that allows you to play your favorite mods, and keep them up to date, all in one neat little package.
License:        GPL-3.0-or-later
URL:            https://modrinth.com/app
Source0:        https://github.com/modrinth/code/archive/refs/tags/v%{version}.tar.gz
Source1:        modrinth-app.desktop
Source2:        modrinth-app

BuildRequires:  rust cargo glib2-devel rust-gdk-devel openssl-devel dbus-devel freetype-devel gtk3-devel libappindicator-gtk3-devel rust-librsvg-devel libsoup-devel webkit2gtk3-devel mesa-libGL-devel pulseaudio-libs-devel libX11-devel libXcursor-devel libXext-devel libXxf86vm-devel
BuildRequires:  pnpm

%description
An unique, open source launcher that allows you to play your favorite mods, and keep them up to date, all in one neat little package.

%prep
%setup -q -n code-%{version}
mkdir theseus_gui/dist

%build
CARGO_TARGET_DIR=target RUSTUP_TOOLCHAIN=stable cargo fetch --locked --target "%{_arch}-unknown-linux-gnu"
cd theseus_gui
COREPACK_ENABLE_STRICT=0 pnpm install
cd ..
CARGO_TARGET_DIR=target RUSTUP_TOOLCHAIN=stable cargo build --frozen --release --all-features

%install
install -Dm755 %{SOURCE2} %{buildroot}/usr/bin/modrinth-app
install -Dm755 %{_builddir}/code-%{version}/target/release/theseus_gui %{buildroot}/opt/modrinth-app/modrinth-app

install -Dm644 %{_builddir}/code-%{version}/theseus_gui/src-tauri/icons/128x128.png %{buildroot}/usr/share/icons/hicolor/128x128/apps/modrinth-app.png
install -Dm644 %{_builddir}/code-%{version}/theseus_gui/src-tauri/icons/icon.png %{buildroot}/usr/share/icons/hicolor/256x256@2/apps/modrinth-app.png
install -Dm644 %{SOURCE1} %{buildroot}/usr/share/applications/modrinth-app.desktop

%files
%{_bindir}/modrinth-app
/opt/modrinth-app/modrinth-app
%{_datadir}/icons/hicolor/128x128/apps/modrinth-app.png
%{_datadir}/icons/hicolor/256x256@2/apps/modrinth-app.png
%{_datadir}/applications/modrinth-app.desktop

%changelog
%autochangelog
