Summary:	A modular geoinformation service
Summary(pl.UTF-8):	Modularna usługa geoinformacyjna
Name:		geoclue2
Version:	2.0.0
Release:	2
License:	GPL v2+
Group:		Applications
Source0:	http://www.freedesktop.org/software/geoclue/releases/2.0/geoclue-%{version}.tar.xz
# Source0-md5:	401ff99d530b177c62afacef0a33efd9
URL:		http://geoclue.freedesktop.org/
BuildRequires:	GeoIP-devel >= 1.5.1
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.34.0
BuildRequires:	gnome-common
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	json-glib-devel >= 0.14
BuildRequires:	libsoup-devel >= 2.4.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	sed >= 4.0
BuildRequires:	yelp-tools
Requires:	GeoIP >= 1.5.1
Requires:	dbus
Requires:	glib2 >= 1:2.34.0
Requires:	json-glib >= 0.14
Requires:	libsoup >= 2.4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Geoclue is a modular geoinformation service built on top of the D-Bus
messaging system. The goal of the Geoclue project is to make creating
location-aware applications as simple as possible.

%description -l pl.UTF-8
Geoclue to modularna usługa geoinformacyjna zbudowana w oparciu o
system komunikacji D-Bus. Celem projektu jest jak największe
ułatwienie tworzenia aplikacji uwzględniających lokalizację.

%package devel
Summary:	Development package for geoclue2
Summary(pl.UTF-8):	Pakiet programistyczny geoclue2
Group:		Development/Libraries
# doesn't require base
Requires:	glib2-devel >= 1:2.34.0
Requires:	json-glib-devel >= 0.14
Requires:	libsoup-devel >= 2.4.0

%description devel
Header files for development with geoclue2.

%description devel -l pl.UTF-8
Pliki nagłówkowe do programowania z użyciem geoclue2.

%prep
%setup -q -n geoclue-%{version}

%{__sed} -i -e '/po\/Makefile.in/d' -e '/IT_PROG_INTLTOOL/d' configure.ac
%{__sed} -i -e 's/ po docs$/ docs/' Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_bindir}/geoip-lookup
%attr(755,root,root) %{_bindir}/geoip-update
%attr(755,root,root) %{_libexecdir}/geoclue
/etc/dbus-1/system.d/org.freedesktop.GeoClue2.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.GeoClue2.service

%files devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/geoclue-2.0.pc
%dir %{_datadir}/geoclue-2.0
%{_datadir}/geoclue-2.0/geoclue-interface.xml
