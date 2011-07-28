Name:			atari800
Version:		2.2.1
Release:		%mkrel 1

Summary:	Atari 800 Emulator
License:	GPLv2+
Group:		Emulators
Source0:	http://downloads.sourceforge.net/atari800/atari800-%{version}.tar.gz
Source1:	%{name}-chooser
URL:		http://atari800.atari.org/

BuildRequires:	SDL-devel
BuildRequires:	XFree86-devel
BuildRequires:	zlib-devel
BuildRequires:	termcap-devel
BuildRequires:	ncurses-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
This is Atari 800, 800XL, 130XE and 5200 emulator.

%package common
Summary:	Atari 800 Emulator - common files for all versions
Group:		Emulators
License:	GPLv2+

%description common
This is Atari 800, 800XL, 130XE and 5200 emulator.

This package contains common files for ncurses, SDL and X11 versions
of Atari800.

This emulator requires atari bios files to operate.
Unfortunately, these files cannot be distributed with this package due to 
license concerns. However, to avoid dumping these files yourself, you can 
download these from http://prdownloads.sf.net/atari800/xf25.zip and then 
put the roms ("*.ROM files") in the /usr/share/atari800 directory.

%package x11
Summary:	Atari 800 Emulator - X Window version
License:	GPLv2+
Group:		Emulators
Requires:	%{name}-common = %{version}

%description x11
This is Atari 800, 800XL, 130XE and 5200 emulator.

This package contains Atari800 executable file configured for X11 with
sound and joystick support.

%package sdl
Summary:	Atari 800 Emulator - SDL version
License:	GPLv2+
Group:		Emulators
Requires:	%{name}-common = %{version}
Obsoletes:	%{name}-SDL

%description sdl
This is Atari 800, 800XL, 130XE and 5200 emulator.

This package contains Atari800 executable file configured for SDL with
sound and joystick support.

%package ncurses
Summary:	Atari 800 Emulator - Ncurses version
License:	GPLv2+
Group:		Emulators
Requires:	%{name}-common = %{version}
Obsoletes:	%{name}-svga

%description ncurses
This is Atari 800, 800XL, 130XE and 5200 emulator.

This package contains Atari800 executable file configured for Ncurses 
support.


%prep
%setup -q -n atari800-%{version}
find ./src -type f -name "*.[chi]*" -exec chmod 644 '{}' +

%build
cd src
aclocal
autoconf

%configure --target=sdl 
%make
mv -f atari800 atari800-sdl
make clean

%configure --target=shm 
%make
mv -f atari800 atari800-x11
make clean

%configure --target=ncurses
%make
mv -f atari800 atari800-ncurses

%install
rm -rf %{buildroot}
install -d %{buildroot}{%{_bindir},%{_datadir}/atari800,%{_mandir}/man1}
install src/atari800-x11 %{buildroot}%{_bindir}
install src/atari800-sdl %{buildroot}%{_bindir}
install src/atari800-ncurses %{buildroot}%{_bindir}
install %{SOURCE1} %{buildroot}%{_bindir}/atari800
install src/atari800.man %{buildroot}%{_mandir}/man1/atari800.1

%clean
rm -rf %{buildroot}

%files common
%defattr(644,root,root,755)
%doc DOC/{BUGS,CREDITS,ChangeLog,FAQ,NEWS,README,TODO,USAGE,*.txt} README.1ST
%attr(755,root,root) %{_bindir}/atari800
%{_datadir}/atari800
%{_mandir}/man1/atari800.1*

%files x11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/atari800-x11

%files sdl 
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/atari800-sdl

%files ncurses
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/atari800-ncurses

