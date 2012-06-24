
# Conditional build:
%bcond_without	status_bar  # do not add status bar options to /etc/screenrc

Summary:	Screen - Manages multiple sessions on one tty
Summary(de):	Screen - Verwaltet mehrere Sitzungen an einem tty
Summary(es):	Screen - Administra m�ltiples sesiones en un tty
Summary(fr):	screen - g�re plusieurs sessions sur un seul terminal
Summary(pl):	Screen - Program zarz�dzaj�cy sesjami na jednym terminalu
Summary(pt_BR):	Screen - Gerencia m�ltiplas sess�es em um tty
Summary(ru):	�������� ������, �������������� ��������� ������� � ������ ���������
Summary(tr):	Bir u�birimde birden fazla oturumu d�zenler
Summary(uk):	�������� ������, �� Ц�����դ ˦���� ��ǦΦ� � ������ ���ͦ����
Name:		screen
Version:	4.0.2
Release:	4
License:	GPL
Group:		Applications/Terminal
Source0:	ftp://ftp.uni-erlangen.de/pub/utilities/screen/%{name}-%{version}.tar.gz
# Source0-md5:	ed68ea9b43d9fba0972cb017a24940a1
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source1-md5:	236166e774cee788cf594b05dd1dd70d
Source2:	%{name}.pamd
Patch0:		%{name}-tty.patch
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
Patch11:	%{name}-status-bar.patch
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

%description -l de
Screens ist ein Programm, das Ihnen erlaubt, sich auf einem Terminal
mehrfach einzuloggen - was n�tzlich sein kann, wenn Sie �ber ein
dummes Terminal eine Telnetverbindung zu einem Rechner haben und mehr
als ein Login ben�tigen.

%description -l es
Screen es un programa que permite que tengas m�ltiples logins en un
terminal. Es �til en situaciones donde est�s usando telnet en una
m�quina o conectado v�a un terminal dumb y quiera m�s que apenas un
login.

%description -l fr
Screen est un programme permettant plusieurs connexions sur un
terminal. Il est utile pour ouvrir plusieurs sessions � la fois, si
vous voulez ouvrir une session telnet sur une autre machine et voulez
plus d'une connexion.

%description -l pl
Screen jest programem, kt�ry umo�liwia otworzenie wielu sesji na
jednym terminalu. Jest to bardzo przydatne, przy po��czeniach z
terminali nie umo�liwiaj�cych otwarcia kilku sesji w systemie. Screen
umo�liwia ponadto powr�t do otwartych sesji w przypadku przerwania
po��czenia z terminalem.

%description -l pt_BR
Screen � um programa que permite que voc� tenha m�ltiplos logins em um
terminal. Ele � �til em situa��es onde voc� est� usando telnet em uma
m�quina ou conectado via um terminal dumb e quer mais do que apenas um
login.

%description -l ru
������� screen ��������� ����� ��������� ������ �� ����� ���������.
Screen ������� �������������, ������� ������� �� ������ �� ���� ���
����� dumb-��������, �� ����� ����� ����� ����� ������ � ���� �������.

%description -l tr
Screen, ayn� u�birimde birden fazla oturum olana�� sa�layan bir
programd�r. Bir makinaya telnet program� ile ya da programlanamaz bir
u�birim �zerinden ba�lant� kurdu�unuz durumlarda kullan��l�d�r.

%description -l uk
���̦�� screen ������Ѥ ���� ��˦���� ��Ӧ� �� ������ ���ͦ��̦.
Screen �������� ������������, �˦ �������� �� ������ �� ����֦ ���
����� dumb-���ͦ���, ��� ������ ���� ¦���� ���ϧ ��Ӧ� � æ��
�������.

%prep
%setup -q
%patch0 -p1
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
%{?with_status_bar:%patch11 -p1}

%build
%{__aclocal}
%{__autoconf}
%configure \
	--with-sys-screenrc=%{_sysconfdir}/screenrc \
	--enable-pam \
	--enable-colors256 \
	--disable-socket-dir

for file in *.dist; do
filenew=$(echo "$file" | sed -e 's#\.dist##g')
	cp -f $file $filenew
done

%{__make} \
	CFLAGS="%{rpmcflags}"

cd doc
rm -f screen.info*
makeinfo screen.texinfo

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/screen/utf8encodings} \
	$RPM_BUILD_ROOT{/etc/{skel,pam.d},%{_mandir}/{,pl}/man1,%{_infodir}}

install screen			$RPM_BUILD_ROOT%{_bindir}
install doc/screen.1		$RPM_BUILD_ROOT%{_mandir}/man1
install doc/screen.info*	$RPM_BUILD_ROOT%{_infodir}
install etc/etcscreenrc		$RPM_BUILD_ROOT%{_sysconfdir}/screenrc
install etc/screenrc		$RPM_BUILD_ROOT/etc/skel/.screenrc
install utf8encodings/*		$RPM_BUILD_ROOT%{_datadir}/screen/utf8encodings

bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
install %{SOURCE2}		$RPM_BUILD_ROOT/etc/pam.d/screen

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc NEWS README ChangeLog doc/{FAQ,README.DOTSCREEN}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/screenrc
%attr(755,root,root) %{_bindir}/screen
%{_datadir}/screen
%attr(600,root,root) /etc/skel/.screenrc
%{_mandir}/man1/*
%lang(ja) %{_mandir}/ja/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%{_infodir}/screen.info*
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*
