Summary:	Screen - Manages multiple sessions on one tty
Summary(de):	Screen - Verwaltet mehrere Sitzungen an einem tty
Summary(fr):	screen - gère plusieurs sessions sur un seul terminal
Summary(pl):	Screen - Program zarz±dzaj±cy sesjami na jednym terminalu
Summary(tr):	Bir uçbirimde birden fazla oturumu düzenler
Name:		screen
Version:	3.9.10
Release:	5
License:	GPL
Group:		Applications/Terminal
Source0:	ftp://ftp.uni-erlangen.de/pub/utilities/screen/%{name}-%{version}.tar.gz
Source1:	%{name}-non-english-man-pages.tar.bz2
Source2:	%{name}.pamd
Patch0:		%{name}-tty.patch
Patch1:		%{name}-compat21.patch
Patch2:		%{name}-DESTDIR.patch
Patch3:		%{name}-manual.patch
Patch4:		%{name}-ia64.patch
Patch5:		%{name}-info.patch
Patch6:		%{name}-debian.patch
Patch7:		%{name}-nolibtermcap.patch
Patch8:		%{name}-no_hardcoded_term_sequences.patch
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	utempter-devel
BuildRequires:	texinfo
BuildRequires:	pam-devel
BuildRequires:	autoconf
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
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p0
%patch4 -p0
%patch5 -p1
%patch6 -p1
%patch7 -p1
#%patch8 -p1

%build
autoconf
%configure \
	--with-sys-screenrc=%{_sysconfdir}/screenrc \
	--with-libpam \
	--disable-socket-dir

%{__make} CFLAGS="%{rpmcflags}"
(cd doc; rm -f screen.info*; makeinfo screen.texinfo)

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/{skel,pam.d},%{_bindir},%{_mandir}/{,pl}/man1,%{_infodir}}

install screen			$RPM_BUILD_ROOT%{_bindir}
install doc/screen.1		$RPM_BUILD_ROOT%{_mandir}/man1
install doc/screen.info*	$RPM_BUILD_ROOT%{_infodir}
install etc/etcscreenrc		$RPM_BUILD_ROOT%{_sysconfdir}/screenrc
install etc/screenrc		$RPM_BUILD_ROOT/etc/skel/.screenrc

bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
install %{SOURCE2}		$RPM_BUILD_ROOT/etc/pam.d/screen

gzip -9nf NEWS README FAQ ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc *.gz
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/screenrc
%attr(755,root,root) %{_bindir}/screen
%attr(600,root,root) /etc/skel/.screenrc
%{_mandir}/man1/*
%lang(ja) %{_mandir}/ja/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%{_infodir}/screen.info*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/*
