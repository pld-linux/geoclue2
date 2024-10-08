#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	A modular geoinformation service
Summary(pl.UTF-8):	Modularna usługa geoinformacyjna
Name:		geoclue2
Version:	2.7.2
Release:	1
License:	GPL v2+ (programs), LGPL v2.1+ (library)
Group:		Applications
#Source0Download: https://gitlab.freedesktop.org/geoclue/geoclue/-/tags
Source0:	https://gitlab.freedesktop.org/geoclue/geoclue/-/archive/%{version}/geoclue-%{version}.tar.bz2
# Source0-md5:	d58d6f3286a6b3ace395fc36468aace2
URL:		https://geoclue.freedesktop.org/
BuildRequires:	ModemManager-devel >= 1.12
BuildRequires:	avahi-devel >= 0.6.10
BuildRequires:	avahi-glib-devel >= 0.6.10
BuildRequires:	glib2-devel >= 1:2.74.0
BuildRequires:	gobject-introspection-devel >= 0.10
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	gtk-doc-automake >= 1.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	json-glib-devel >= 0.14
BuildRequires:	libnotify-devel
BuildRequires:	libsoup3-devel >= 3.0.0
BuildRequires:	meson >= 0.60.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	yelp-tools
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	ModemManager-libs >= 1.12
Requires:	avahi-libs >= 0.6.10
Requires:	avahi-glib >= 0.6.10
Requires:	dbus
Requires:	json-glib >= 0.14
Requires:	libsoup3 >= 3.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Geoclue is a modular geoinformation service built on top of the D-Bus
messaging system. The goal of the Geoclue project is to make creating
location-aware applications as simple as possible.

%description -l pl.UTF-8
Geoclue to modularna usługa geoinformacyjna zbudowana w oparciu o
system komunikacji D-Bus. Celem projektu jest jak największe
ułatwienie tworzenia aplikacji uwzględniających lokalizację.

%package libs
Summary:	Library to interact with Geoclue service
Summary(pl.UTF-8):	Biblioteka do współpracy z usługą Geoclue
License:	LGPL v2.1+
Group:		Libraries
Requires:	glib2 >= 1:2.74.0

%description libs
Library to interact with Geoclue service.

%description libs -l pl.UTF-8
Biblioteka do współpracy z usługą Geoclue.

%package devel
Summary:	Development package for geoclue2
Summary(pl.UTF-8):	Pakiet programistyczny geoclue2
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.74.0

%description devel
Header files for development with geoclue2.

%description devel -l pl.UTF-8
Pliki nagłówkowe do programowania z użyciem geoclue2.

%package static
Summary:	Static geoclue2 library
Summary(pl.UTF-8):	Statyczna biblioteka geoclue2
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static geoclue2 library.

%description static -l pl.UTF-8
Statyczna biblioteka geoclue2.

%package -n vala-geoclue2
Summary:	Vala API for geoclue2 library
Summary(pl.UTF-8):	Interfejs języka Vala do biblioteki geoclue2
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
BuildArch:	noarch

%description -n vala-geoclue2
Vala API for geoclue2 library.

%description -n vala-geoclue2 -l pl.UTF-8
Interfejs języka Vala do biblioteki geoclue2.

%package apidocs
Summary:	API documentation for geoclue2 library
Summary(pl.UTF-8):	Dokumentacja API biblioteki geoclue2
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for geoclue2 library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki geoclue2.

%prep
%setup -q -n geoclue-%{version}

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	-Dsystemd-system-unit-dir=%{systemdunitdir}

# TODO: -Ddbus-srv-user= (nonroot)

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# resolve conflict with geoclue-apidocs 0.12.x
%{__mv} $RPM_BUILD_ROOT%{_gtkdocdir}/geoclue{,-2.0}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_libexecdir}/geoclue
%dir %{_sysconfdir}/geoclue
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/geoclue/geoclue.conf
%{systemdunitdir}/geoclue.service
%{_datadir}/dbus-1/system.d/org.freedesktop.GeoClue2.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.GeoClue2.Agent.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.GeoClue2.service
%{_datadir}/polkit-1/rules.d/org.freedesktop.GeoClue2.rules
# demos
/etc/xdg/autostart/geoclue-demo-agent.desktop
%dir %{_libexecdir}/geoclue-2.0
%dir %{_libexecdir}/geoclue-2.0/demos
%attr(755,root,root) %{_libexecdir}/geoclue-2.0/demos/agent
%attr(755,root,root) %{_libexecdir}/geoclue-2.0/demos/where-am-i
%{_desktopdir}/geoclue-demo-agent.desktop
%{_desktopdir}/geoclue-where-am-i.desktop
%{_mandir}/man5/geoclue.5*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgeoclue-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgeoclue-2.so.0
%{_libdir}/girepository-1.0/Geoclue-2.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgeoclue-2.so
%{_includedir}/libgeoclue-2.0
%{_datadir}/gir-1.0/Geoclue-2.0.gir
%{_pkgconfigdir}/geoclue-2.0.pc
%{_pkgconfigdir}/libgeoclue-2.0.pc
%{_datadir}/dbus-1/interfaces/org.freedesktop.GeoClue2.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.GeoClue2.Agent.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.GeoClue2.Client.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.GeoClue2.Location.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.GeoClue2.Manager.xml

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgeoclue-2.a
%endif

%files -n vala-geoclue2
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libgeoclue-2.0.deps
%{_datadir}/vala/vapi/libgeoclue-2.0.vapi

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/geoclue-2.0
%{_gtkdocdir}/libgeoclue
