Summary:     Screen - Manages multiple sessions on one tty
Summary(de): Screen - Verwaltet mehrere Sitzungen an einem tty
Summary(fr): screen - gère plusieurs sessions sur un seul terminal
Summary(pl): Screen - Program zarz±dzaj±cy wieloma sesjami na jednym terminalu
Summary(tr): Bir uçbirimde birden fazla oturumu düzenler
Name:        screen
Version:     3.7.4
Release:     4
Copyright:   GPL
Group:       Utilities/Terminal
Source:      ftp://prep.ai.mit.edu/pub/gnu/%{name}-%{version}.tar.gz
Patch0:      screen-3.6.2.patch
Patch1:      screen-3.7.3-linux.patch
Patch2:      screen-3.7.1-glibc.patch
Patch3:      screen-3.7.3-tty.patch
Patch4:	     screen-tmprace.patch
Prereq:      /sbin/install-info
BuildRoot:   /tmp/%{name}-%{version}-root

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
%patch0
%patch1 -p1

%ifarch axp
%patch2 -p1
%endif

%patch3 -p1 
%patch4 -p1

%build
./configure --prefix=/usr
make CC="gcc $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/skel,usr/{bin,man/man1,info}}

install -s screen $RPM_BUILD_ROOT/usr/bin
install doc/screen.1 $RPM_BUILD_ROOT/usr/man/man1
install doc/screen.info* $RPM_BUILD_ROOT/usr/info
install etc/etcscreenrc $RPM_BUILD_ROOT/etc/screenrc
install etc/screenrc $RPM_BUILD_ROOT/etc/skel/.screenrc

gzip -9nf $RPM_BUILD_ROOT/usr/info/screen.info*

%post
/sbin/install-info /usr/info/screen.info.gz /usr/info/dir --entry \
"* screen: (screen).                             Terminal multiplexer."

%preun
/sbin/install-info --delete /usr/info/screen.info.gz /usr/info/dir --entry \
"* screen: (screen).                             Terminal multiplexer."

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644, root, root, 755)
%doc NEWS README FAQ ChangeLog
%attr(4755, root, root) /usr/bin/screen
%attr(0644, root,  man) /usr/man/man1/*
/usr/info/screen.info*
%config(noreplace) %verify(not md5 mtime size) /etc/skel/.screenrc
%config(noreplace) %verify(not md5 mtime size) /etc/screenrc

%changelog
* Sun Nov 22 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [3.7.4-4]
- changed to %attr(0644, root,  man) on man pages in %files,
- fixed --entry text on {un}registering info page for ed in %post
  %preun in devel.

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
