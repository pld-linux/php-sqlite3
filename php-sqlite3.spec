%define		_modname	sqlite3
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
Summary:	%{_modname} - database bindings
Summary(pl):	%{_modname} - powi±zania z baz± danych
Name:		php-%{_modname}
Version:	0.4
Release:	0.1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://dl.sourceforge.net/sourceforge/php-sqlite3/%{_modname}-%{version}.tgz
# Source0-md5:	fc15ace3f5fd0aac0186745d6cff8a70
URL:		http://php-sqlite3.sourceforge.net/pmwiki/pmwiki.php
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	sqlite3-devel >= 3.3.5
BuildRequires:	rpmbuild(macros) >= 1.322
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
%{_modname} is a C library that implements an embeddable SQL database
engine. Programs that link with the %{_modname} library can have SQL
database access without running seperate RDBMS process. This extension
allows you to access %{_modname} databases from within PHP.

%description -l pl
%{_modname} jest napisan± w C bibliotek± implementuj±c± osadzon± bazê
SQL. Programy konsolidowane z %{_modname} mog± mieæ dostêp do bazy SQL
bez potrzeby uruchamiana kolejnego procesu RDBMS. To rozszerzenie
pozwala na dostêp do baz SQLite z poziomu PHP.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure \
	--with-sqlite3=shared,/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

#chmod 755 build/shtool
%{__make} -C %{_modname}-%{version} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_smodname}.ini
; Enable %{_modname} extension module
extension=%{_smodname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/README %{_modname}-%{version}/TODO %{_modname}-%{version}/CREDITS
%doc %{_modname}-%{version}/sqlite.php %{_modname}-%{version}/tests
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_smodname}.ini
%attr(755,root,root) %{extensionsdir}/%{_smodname}.so
