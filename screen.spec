Summary:	Screen - Manages multiple sessions on one tty
Summary(de):	Screen - Verwaltet mehrere Sitzungen an einem tty
Summary(fr):	screen - gère plusieurs sessions sur un seul terminal
Summary(pl):	Screen - Program zarz±dzaj±cy sesjami na jednym terminalu
Summary(tr):	Bir uçbirimde birden fazla oturumu düzenler
Name:		screen
Version:	3.9.8
Release:	1
License:	GPL
Group:		Utilities/Terminal
Group(pl):	Narzêdzia/Terminal
Source0:	ftp://ftp.uni-erlangen.de/pub/utilities/screen/%{name}-%{version}.tar.gz
Patch0:		screen-info.patch
Patch1:		screen-tty.patch
Patch2:		screen-compat21.patch
Patch3:		screen-DESTDIR.patch
Patch4:		screen-doc_fixes.patch
Patch5:		screen-texinfo_doc_fixes.patch
Patch6:		screen-home_etc.patch
Patch7:		screen-ia64.patch
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	utempter-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
Screen is a program that allows you to have multiple logins on one
terminal. It is useful in situations where you are telnetted into a
machine or connected via a dumb terminal and want more than just one
login.

%description -l de
Screens ist ein Programm, das Ihnen erlaubt, sich auf einem Terminal
mehrfach einzuloggen - was nützlich sein kann, wenn Sie über ein
dummes Terminal eine Telnetverbindung zu einem Rechner haben und mehr
als ein Login benötigen.

%description -l fr
Screen est un programme permettant plusieurs connexions sur un
terminal. Il est utile pour ouvrir plusieurs sessions à la fois, si
vous voulez ouvrir une session telnet sur une autre machine et voulez
plus d'une connexion.

%description -l pl
Screen jest programem, który umo¿liwia otworzenie wielu sesji na
jednym terminalu. Jest to bardzo przydatne, przy po³±czeniach z
terminali nie umo¿liwiaj±cych otwarcia kilku sesji w systemie. Screen
umo¿liwia ponadto powrót do otwartych sesji w przypadku przerwania
po³±czenia z terminalem.

%description -l tr
Screen, ayný uçbirimde birden fazla oturum olanaðý saðlayan bir
programdýr. Bir makinaya telnet programý ile ya da programlanamaz bir
uçbirim üzerinden baðlantý kurduðunuz durumlarda kullanýþlýdýr.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
LDFLAGS="-s"; export LDFLAGS
%configure

%{__make} CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE" 
(cd doc; rm -f screen.info*; makeinfo screen.texinfo)

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/skel,%{_bindir},%{_mandir}/man1,%{_infodir}}

install -s screen $RPM_BUILD_ROOT%{_bindir}
install doc/screen.1 $RPM_BUILD_ROOT%{_mandir}/man1
install doc/screen.info* $RPM_BUILD_ROOT%{_infodir}
install etc/etcscreenrc $RPM_BUILD_ROOT%{_sysconfdir}/screenrc
install etc/screenrc $RPM_BUILD_ROOT/etc/skel/.screenrc

gzip -9nf $RPM_BUILD_ROOT/{%{_infodir}/screen.info*,%{_mandir}/man1/*} \
	NEWS README FAQ ChangeLog

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/screenrc
%attr(755,root,root) %{_bindir}/screen
%{_mandir}/man1/*
%{_infodir}/screen.info*
