Summary:	Screen - Manages multiple sessions on one tty
Summary(de):	Screen - Verwaltet mehrere Sitzungen an einem tty
Summary(fr):	screen - gère plusieurs sessions sur un seul terminal
Summary(pl):	Screen - Program zarz±dzaj±cy sesjami na jednym terminalu
Summary(tr):	Bir uçbirimde birden fazla oturumu düzenler
Name:		screen
Version:	3.7.6
Release:	3
Copyright:	GPL
Group:		Utilities/Terminal
Group(pl):	U¿ytki/Terminal
Source:		ftp://ftp.gnu.org/pub/gnu/%{name}-%{version}.tar.gz
Patch0:		screen.patch
Patch1:		screen-linux.patch
Patch2:		screen-utmp.patch
Patch3:		screen-info.patch
Prereq:		/sbin/install-info
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Screen is a program that allows you to have multiple
logins on one terminal.  It is useful in situations where
you are telnetted into a machine or connected via a dumb
terminal and want more than just one login.

%description -l de
Screens ist ein Programm, das Ihnen erlaubt, sich auf einem
Terminal mehrfach einzuloggen - was nützlich sein kann,
wenn Sie über ein dummes Terminal eine Telnetverbindung zu
einem Rechner haben und mehr als ein Login benötigen.

%description -l fr
Screen est un programme permettant plusieurs connexions sur un terminal.
Il est utile pour ouvrir plusieurs sessions à la fois, si vous voulez
ouvrir une session telnet sur une autre machine et voulez plus d'une
connexion.

%description -l pl
Screen jest programem, który umo¿liwia otworzenie wielu sesji na jednym
terminalu. Jest to bardzo przydatne, przy po³±czeniach z terminali nie
umo¿liwiaj±cych otwarcia kilku sesji w systemie. Screen umo¿liwia ponadto
powrót do otwartych sesji w przypadku przerwania po³±czenia z terminalem.

%description -l tr
Screen, ayný uçbirimde birden fazla oturum olanaðý saðlayan bir programdýr.
Bir makinaya telnet programý ile ya da programlanamaz bir uçbirim üzerinden
baðlantý kurduðunuz durumlarda kullanýþlýdýr.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
./configure %{_target} \
    --prefix=/usr

make CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE" 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/skel,usr/{bin,man/man1,info}}

install -s screen $RPM_BUILD_ROOT%{_bindir}
install doc/screen.1 $RPM_BUILD_ROOT%{_mandir}/man1
install doc/screen.info* $RPM_BUILD_ROOT%{_infodir}
install etc/etcscreenrc $RPM_BUILD_ROOT/etc/screenrc
install etc/screenrc $RPM_BUILD_ROOT/etc/skel/.screenrc

gzip -9nf $RPM_BUILD_ROOT/usr/{info/screen.info*,man/man1/*} \
	NEWS README FAQ ChangeLog

%post
/sbin/install-info %{_infodir}/screen.info.gz /etc/info-dir

%preun
if [ "$1" = "0" ]; then
	/sbin/install-info --delete %{_infodir}/screen.info.gz /etc/info-dir
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz

%attr(755,root,root) %{_bindir}/screen
%{_mandir}/man1/*

%{_infodir}/screen.info*

%config(noreplace) %verify(not md5 mtime size) /etc/screenrc

%changelog
* Mon Mar 29 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [3.7.6-3]
- removed man group from man pages,
- standarized {un}registering info pages (added screen-info.patch).

* Fri Feb 05 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [3.7.6-2d]
- added utpm patch. 

* Thu Oct 01 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [3.7.4-3d]
- build against Tornado,
- restricted files permission,
- changed man pages group to man,
- minor modifications of the spec file.

* Sun Aug 23 1998 Marcin Bohosiewicz <marcus@krakow.linux.org.pl>
  [3.7.4-3]
- added translations de,fr,tr from orginal RH 5.1 screen's spec,
- added pl translation,
- added %defattr support,
- added %post and %preun scripts from RH 5.1 screen's spec,
- removed INSTALL from %doc,
- added %verify rules for %config files,
- added -q %setup parameter,
- added using $RPM_OPT_FLAGS during compile,
- changed copyright statment to GPL,
- changed %%{PACKAGE_VERSION} to %%{version} and %%{name} macros.

* Wed Aug 19 1998 Marcin Bohosiewicz <marcus@krakow.linux.org.pl>
  [3.7.4-2]
- added tmprace-fix from BUGTRAQ list

* Sun Aug 17 1997 Marcin Bohosiewicz <marcus@krakow.linux.org.pl>
  [3.7.4-1]
- added %%{PACKAGE_VERSION} macro to Source,
- all rewrited for using Buildroot,
- added #define PTYGROUP 5 and #define PTYMODE 0620 in config.h.in
  gid=5 is tty group in RedHat Linux (/dev/tty* used by screen is not
  curently writable by other users), 
- added striping screen binary,
- added %attr macros in %files (allow build package from non root
  account),
- added %clear section.
