#
# Conditional build:
%bcond_with	fifo		# force using fifos even if sockets detected

# TODO
# - should we switch back fifos forcibly (so you could resume 4.0 sessions with 4.1?, stalled for me anyway)
#   configure: checking socket implementation...
#   - you are normal
#   - both sockets and fifos usable. let's take sockets.
Summary:	Screen - Manages multiple sessions on one tty
Summary(de.UTF-8):	Screen - Verwaltet mehrere Sitzungen an einem tty
Summary(es.UTF-8):	Screen - Administra múltiples sesiones en un tty
Summary(fr.UTF-8):	screen - gère plusieurs sessions sur un seul terminal
Summary(pl.UTF-8):	Screen - Program zarządzający sesjami na jednym terminalu
Summary(pt_BR.UTF-8):	Screen - Gerencia múltiplas sessões em um tty
Summary(ru.UTF-8):	Менеджер экрана, поддерживающий несколько логинов с одного терминала
Summary(tr.UTF-8):	Bir uçbirimde birden fazla oturumu düzenler
Summary(uk.UTF-8):	Менеджер екрану, що підтримує кілька логінів з одного терміналу
Name:		screen
Version:	4.1.0
Release:	1.1
License:	GPL v3+
Group:		Applications/Terminal
Source0:	http://git.savannah.gnu.org/cgit/screen.git/snapshot/screen-a805439f6443fb0e00ac6caff92f99950c1ddda8.tar.gz
# Source0-md5:	1aca27adebec4ab0c3a8ee683675a7fd
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source1-md5:	236166e774cee788cf594b05dd1dd70d
Source2:	%{name}.pamd
Source3:	screenrc
Patch1:		%{name}-compat21.patch
Patch2:		%{name}-manual.patch
Patch3:		%{name}-ia64.patch
Patch4:		%{name}-info.patch
Patch5:		%{name}-debian_fixed.patch
Patch6:		%{name}-nolibtermcap.patch
Patch7:		%{name}-no_hardcoded_term_sequences.patch
Patch8:		%{name}-home_etc.patch
Patch9:		%{name}-no-libs.patch
Patch10:	%{name}-varargs.patch
Patch11:	%{name}-inputline-size.patch
Patch12:	%{name}-screenrc.patch
Patch13:	%{name}-osc.patch
Patch15:	%{name}-statusline-encoding.patch
URL:		http://www.gnu.org/software/screen/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	pam-devel
BuildRequires:	texinfo
BuildRequires:	utempter-devel
Requires:	pam >= 0.77.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Screen is a program that allows you to have multiple logins on one
terminal. It is useful in situations where you are telnetted into a
machine or connected via a dumb terminal and want more than just one
login.

%description -l de.UTF-8
Screens ist ein Programm, das Ihnen erlaubt, sich auf einem Terminal
mehrfach einzuloggen - was nützlich sein kann, wenn Sie über ein
dummes Terminal eine Telnetverbindung zu einem Rechner haben und mehr
als ein Login benötigen.

%description -l es.UTF-8
Screen es un programa que permite que tengas múltiples logins en un
terminal. Es útil en situaciones donde estás usando telnet en una
máquina o conectado vía un terminal dumb y quiera más que apenas un
login.

%description -l fr.UTF-8
Screen est un programme permettant plusieurs connexions sur un
terminal. Il est utile pour ouvrir plusieurs sessions à la fois, si
vous voulez ouvrir une session telnet sur une autre machine et voulez
plus d'une connexion.

%description -l pl.UTF-8
Screen jest programem, który umożliwia otworzenie wielu sesji na
jednym terminalu. Jest to bardzo przydatne, przy połączeniach z
terminali nie umożliwiających otwarcia kilku sesji w systemie. Screen
umożliwia ponadto powrót do otwartych sesji w przypadku przerwania
połączenia z terminalem.

%description -l pt_BR.UTF-8
Screen é um programa que permite que você tenha múltiplos logins em um
terminal. Ele é útil em situações onde você está usando telnet em uma
máquina ou conectado via um terminal dumb e quer mais do que apenas um
login.

%description -l ru.UTF-8
Утилита screen позволяет иметь несколько сессий на одном терминале.
Screen полезен пользователям, которые заходят на машину по сети или
через dumb-терминал, но хотят иметь более одной сессии с этой машиной.

%description -l tr.UTF-8
Screen, aynı uçbirimde birden fazla oturum olanağı sağlayan bir
programdır. Bir makinaya telnet programı ile ya da programlanamaz bir
uçbirim üzerinden bağlantı kurduğunuz durumlarda kullanışlıdır.

%description -l uk.UTF-8
Утиліта screen дозволяє мати декілька сесій на одному терміналі.
Screen корисний користувачам, які заходять на машину по мережі або
через dumb-термінал, але хочуть мати більше одної сесії з цією
машиною.

%prep
%setup -qc
mv screen-*/src/* .

%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p1
# DON'T ENABLE IT UNLESS YOU REALLY FIX IT
# (it's heavily broken - note that some sequences should be get for
# $TERM before running screen instance, and others for TERM=screen!)
###%patch7 -p1
#%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
#%patch13 -p1 # my brain farted here, see if you have better luck
%patch15 -p0

%build
%{__aclocal}
%{__autoheader}
%{__autoconf}
CFLAGS="%{rpmcflags} -DMAXWIN=128"
%{?with_fifo:nore=1} \
%configure \
	--enable-pam \
	--enable-colors256 \
	--enable-rxvt_osc \
	--with-sys-screenrc=/etc/screenrc \
	--with-pty-mode=0620 \
	--with-pty-group=5 \
	--disable-socket-dir

%{__make} -j1

cd doc
rm -f screen.info*
makeinfo screen.texinfo

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/screen/utf8encodings} \
	$RPM_BUILD_ROOT{/etc/{skel,pam.d},%{_mandir}/{,pl}/man1,%{_infodir}}

install -p screen $RPM_BUILD_ROOT%{_bindir}
cp -a doc/screen.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -a doc/screen.info* $RPM_BUILD_ROOT%{_infodir}

install etc/etcscreenrc $RPM_BUILD_ROOT%{_sysconfdir}/screenrc
echo -e "\n\n" >> $RPM_BUILD_ROOT%{_sysconfdir}/screenrc
cat %{SOURCE3} > $RPM_BUILD_ROOT%{_sysconfdir}/screenrc

cp -a utf8encodings/* $RPM_BUILD_ROOT%{_datadir}/screen/utf8encodings
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/screen

bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
rm -f $RPM_BUILD_ROOT%{_mandir}/README.screen-non-english-man-pages

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc NEWS README ChangeLog doc/{FAQ,README.DOTSCREEN} etc/screenrc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/screenrc
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*
%attr(755,root,root) %{_bindir}/screen
%{_datadir}/screen
%{_mandir}/man1/*
%lang(ja) %{_mandir}/ja/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%{_infodir}/screen.info*
