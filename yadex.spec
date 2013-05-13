Summary:	Level editor for DOOM
Name:		yadex
Version:	1.7.0
Release:	%mkrel 11
License:	GPL
Group:		Games/Arcade
Source:		http://www.teaser.fr/~amajorel/yadex/%name-%version.tar.bz2
Patch0:		yadex-fix-compil.patch
Patch1:		yadex-1.7.0-gcc45.patch
URL:		http://www.teaser.fr/~amajorel/yadex
BuildRoot:	%_tmppath/%name-%version-%release-root
BuildRequires:	pkgconfig(x11)

%description
Yadex is a Doom level (wad) editor for Unix systems running X, including
Linux. It supports Doom, Doom II, Ultimate Doom, Final Doom, Heretic,
Doom press release pre beta and also, in a more or less limited way, Hexen,
Strife and Doom alpha. It is available under the terms of the GPL.

%prep
%setup -q
%patch0 -p0 -b .fix-compil
%patch1 -p0 -b .gcc

%build
./configure --prefix=%_prefix
%make CXXFLAGS="%optflags" CXX="g++ %ldflags" X11LIBDIR=%{_libdir} X11INCLUDEDIR=%{_includedir}

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

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

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




%changelog
* Fri Jan 21 2011 Funda Wang <fwang@mandriva.org> 1.7.0-11mdv2011.0
+ Revision: 632005
- fix build with latest gcc

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Mon Aug 04 2008 Thierry Vignaud <tv@mandriva.org> 1.7.0-10mdv2009.0
+ Revision: 262772
- rebuild

* Thu Jul 31 2008 Thierry Vignaud <tv@mandriva.org> 1.7.0-9mdv2009.0
+ Revision: 257901
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.7.0-7mdv2008.1
+ Revision: 171193
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 18 2007 Thierry Vignaud <tv@mandriva.org> 1.7.0-6mdv2008.1
+ Revision: 132303
- auto-convert XDG menu entry
- kill re-definition of %%buildroot on Pixel's request


* Mon Jan 15 2007 Olivier Thauvin <nanardon@mandriva.org> 1.7.0-6mdv2007.0
+ Revision: 108974
- patch0: fix build
- Import yadex

* Sat Jan 07 2006 Anssi Hannula <anssi@mandriva.org> 1.7.0-4mdk
- fix x86_64 build

* Fri Oct 21 2005 Olivier Thauvin <nanardon@mandriva.org> 1.7.0-3mdk
- rebuild

* Sat Jul 03 2004 Michael Scherer <misc@mandrake.org> 1.7.0-2mdk 
- rebuild for new gcc

