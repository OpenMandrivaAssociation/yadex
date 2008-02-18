Summary:	Level editor for DOOM
Name:		yadex
Version:	1.7.0
Release:	%mkrel 7
License:	GPL
Group:		Games/Arcade

Source:		http://www.teaser.fr/~amajorel/yadex/%name-%version.tar.bz2
Patch0:     yadex-fix-compil.patch

URL:		http://www.teaser.fr/~amajorel/yadex
BuildRoot:	%_tmppath/%name-%version-%release-root
BuildRequires:	X11-devel

%description
Yadex is a Doom level (wad) editor for Unix systems running X, including
Linux. It supports Doom, Doom II, Ultimate Doom, Final Doom, Heretic,
Doom press release pre beta and also, in a more or less limited way, Hexen,
Strife and Doom alpha. It is available under the terms of the GPL.

%prep
%setup -q
%patch0 -p0 -b .fix-compil

%build
./configure --prefix=%_prefix
%make CXXFLAGS="$RPM_OPT_FLAGS" X11LIBDIR=%{_prefix}/%{_lib}

%install
rm -rf $RPM_BUILD_ROOT
make \
    BINDIR=%buildroot/%_bindir \
    ETCDIR=%buildroot/%_sysconfdir/%name/%version \
    ETCDIRNV=%buildroot/%_sysconfdir/%name \
    MANDIR=%buildroot/%_mandir \
    SHAREDIR=%buildroot/%_datadir/games/%name/%version \
    SHAREDIRNV=%buildroot/games/%_datadir \
        install

mkdir -p ./html
mv ./doc/*.html ./html
mv ./docsrc/*.png ./html
  
cat %buildroot/%_sysconfdir/%name/%version/yadex.cfg | \
	sed -e "s|/usr/local|%_prefix|" > %buildroot/%_sysconfdir/%name/%version/yadex.cfg.tmp

mv %buildroot/%_sysconfdir/%name/%version/yadex.cfg.tmp %buildroot/%_sysconfdir/%name/%version/yadex.cfg

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%name.desktop
[Desktop Entry]
Type=Application
Categories=Game;ArcadeGame;
Name=Yadex
Icon=arcade_section
Comment=A level editor for DOOM
Exec=%name
EOF

%post
%update_menus

%postun
%clean_menus

%clean
rm -fr %buildroot

%files
%defattr(-,root,root)
%doc README TODO CHANGES COPYING COPYING.LIB html
%_bindir/yadex
%_bindir/yadex-%{version}
%dir %_sysconfdir/%name
%dir %_sysconfdir/%name/%version
%config(noreplace) %_sysconfdir/%name/%version/yadex.cfg
%dir %_gamesdatadir/yadex
%dir %_gamesdatadir/yadex/%{version}
%_gamesdatadir/yadex/%{version}/*.ygd
%_mandir/man6/yadex*
%{_datadir}/applications/mandriva-yadex.desktop


