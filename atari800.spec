Summary:	Atari 800 Emulator
Name:		atari800
Version:	4.1.0
Release:	1
License:	GPLv2+
Group:		Emulators
Url:		http://atari800.atari.org/
Source0:	http://downloads.sourceforge.net/atari800/atari800-%{version}-scr.tgz
Source1:	%{name}-chooser
Source2:	ATARI5200.ROM
Source3:	ATARIBAS.ROM
Source4:	ATARIOSA.ROM
Source5:	ATARIOSB.ROM
Source6:	ATARIXL.ROM
#Patch0:		atari800-3.0.0-cfg.patch
BuildRequires:	librsvg
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(zlib)

%description
This is Atari 800, 800XL, 130XE and 5200 emulator.

#----------------------------------------------------------------------------

%package common
Summary:	Atari 800 Emulator - common files for all versions
License:	GPLv2+
Group:		Emulators
Suggests:	%{name}-roms

%description common
This is Atari 800, 800XL, 130XE and 5200 emulator.

This package contains common files for ncurses, SDL and X11 versions
of Atari800.

%files common
%doc DOC/{BUGS,CREDITS,ChangeLog,FAQ,NEWS,README,TODO,USAGE,*.txt} README.1ST
%{_bindir}/%{name}
%{_sysconfdir}/%{name}.cfg
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man1/%{name}.1*

#----------------------------------------------------------------------------

%package roms
Summary:	Atari 800 Emulator - ROM files
License:	Freeware
Group:		Emulators

%description roms
This is Atari 800, 800XL, 130XE and 5200 emulator.

This package contains ROM files.

Notes: Darek Mihocka got the permission from Atari corp. to distribute
the images of Atari 800XL's OS and BASIC ROMs. Package that contains these
ROM images is free now.

%files roms
%{_datadir}/%{name}/*.ROM

#----------------------------------------------------------------------------

%package x11
Summary:	Atari 800 Emulator - X Window version
License:	GPLv2+
Group:		Emulators
Requires:	%{name}-common = %{EVRD}

%description x11
This is Atari 800, 800XL, 130XE and 5200 emulator.

This package contains Atari800 executable file configured for X11 with
sound and joystick support.

%files x11
%{_bindir}/atari800-x11

#----------------------------------------------------------------------------

%package sdl
Summary:	Atari 800 Emulator - SDL version
License:	GPLv2+
Group:		Emulators
Requires:	%{name}-common = %{EVRD}

%description sdl
This is Atari 800, 800XL, 130XE and 5200 emulator.

This package contains Atari800 executable file configured for SDL with
sound and joystick support.

%files sdl
%{_bindir}/atari800-sdl

#----------------------------------------------------------------------------

%package ncurses
Summary:	Atari 800 Emulator - Ncurses version
License:	GPLv2+
Group:		Emulators
Requires:	%{name}-common = %{EVRD}

%description ncurses
This is Atari 800, 800XL, 130XE and 5200 emulator.

This package contains Atari800 executable file configured for Ncurses 
support.

%files ncurses
%{_bindir}/atari800-ncurses

#----------------------------------------------------------------------------

%prep
%setup -q
find ./src -type f -name "*.[chi]*" -exec chmod 644 '{}' +
%patch0 -p1

%build
cd src
aclocal
autoconf

%configure --target=default --with-video=sdl --with-sound=sdl
%make
mv -f atari800 atari800-sdl
make clean

%configure --target=shm
%make
mv -f atari800 atari800-x11
make clean

%configure --target=default --with-video=ncurses
%make
mv -f atari800 atari800-ncurses

%install
mkdir -p %{buildroot}%{_bindir}
install src/atari800-x11 %{buildroot}%{_bindir}
install src/atari800-sdl %{buildroot}%{_bindir}
install src/atari800-ncurses %{buildroot}%{_bindir}
install %{SOURCE1} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_mandir}/man1
install src/atari800.man %{buildroot}%{_mandir}/man1/%{name}.1

mkdir -p %{buildroot}%{_datadir}/%{name}
install -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/%{name}/ATARI5200.ROM
install -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/%{name}/ATARIBAS.ROM
install -m 0644 %{SOURCE4} %{buildroot}%{_datadir}/%{name}/ATARIOSA.ROM
install -m 0644 %{SOURCE5} %{buildroot}%{_datadir}/%{name}/ATARIOSB.ROM
install -m 0644 %{SOURCE6} %{buildroot}%{_datadir}/%{name}/ATARIXL.ROM

mkdir -p %{buildroot}%{_sysconfdir}/
install src/dc/%{name}.cfg %{buildroot}%{_sysconfdir}/%{name}.cfg

# menu-entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Type=Application
Name=Atari800
Name[ru]=Atari800
Comment=An emulator of 8-bit Atari personal computers.
Comment[ru]=Эмулятор 8-bit компьютера Atari
Icon=%{name}
Exec=%{name}
Categories=Game;Emulator;
EOF

# Install icons of various sizes
for s in 256 128 96 48 32 22 16 ; do
mkdir -p %{buildroot}%{_iconsdir}/hicolor/${s}x${s}/apps
rsvg-convert -w ${s} -h ${s} \
    data/atari2.svg -o \
    %{buildroot}%{_iconsdir}/hicolor/${s}x${s}/apps/%{name}.png
done

