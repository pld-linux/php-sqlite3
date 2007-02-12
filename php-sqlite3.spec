%define		_modname	sqlite3
Summary:	%{_modname} - database bindings
Summary(pl.UTF-8):	%{_modname} - powiązania z bazą danych
Name:		php-%{_modname}
Version:	0.4
Release:	0.2
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://dl.sourceforge.net/php-sqlite3/%{_modname}-%{version}.tgz
# Source0-md5:	fc15ace3f5fd0aac0186745d6cff8a70
Patch0:		%{name}-tsrm.patch
Patch1:		%{name}-new-functions.patch
URL:		http://php-sqlite3.sourceforge.net/pmwiki/pmwiki.php
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
BuildRequires:	sqlite3-devel >= 3.3.5
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
sqlite3 is a C library that implements an embeddable SQL database
engine. Programs that link with the sqlite3 library can have SQL
database access without running seperate RDBMS process. This extension
allows you to access sqlite3 databases from within PHP.

%description -l pl.UTF-8
sqlite3 jest napisaną w C biblioteką implementującą osadzoną bazę SQL.
Programy konsolidowane z sqlite3 mogą mieć dostęp do bazy SQL bez
potrzeby uruchamiana kolejnego procesu RDBMS. To rozszerzenie pozwala
na dostęp do baz SQLite z poziomu PHP.

%prep
%setup -q -c
cd %{_modname}-%{version}
%patch0 -p1
%patch1 -p0

%build
cd %{_modname}-%{version}
phpize
%configure \
	--with-sqlite3=shared,/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

#chmod 755 build/shtool
%{__make} -C %{_modname}-%{version} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/README %{_modname}-%{version}/ChangeLog
%doc %{_modname}-%{version}/examples/*
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
