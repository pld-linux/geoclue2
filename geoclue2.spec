#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	A modular geoinformation service
Summary(pl.UTF-8):	Modularna usługa geoinformacyjna
Name:		geoclue2
Version:	2.4.12
Release:	1
License:	GPL v2+ (programs), LGPL v2.1+ (library)
Group:		Applications
Source0:	https://www.freedesktop.org/software/geoclue/releases/2.4/geoclue-%{version}.tar.xz
# Source0-md5:	469bfcebef36723b34aaa5816de93e18
URL:		https://geoclue.freedesktop.org/
BuildRequires:	ModemManager-devel >= 1.6
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	avahi-devel >= 0.6.10
BuildRequires:	avahi-glib-devel >= 0.6.10
BuildRequires:	glib2-devel >= 1:2.44.0
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 0.10
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	json-glib-devel >= 0.14
BuildRequires:	libnotify-devel
BuildRequires:	libsoup-devel >= 2.42
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	tar >= 1:1.22
BuildRequires:	yelp-tools
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	avahi-libs >= 0.6.10
Requires:	avahi-glib >= 0.6.10
Requires:	dbus
Requires:	json-glib >= 0.14
Requires:	libsoup >= 2.42
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
Requires:	glib2 >= 1:2.44.0

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
Requires:	glib2-devel >= 1:2.44.0

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

%description -n vala-geoclue2
Vala API for geoclue2 library.

%description -n vala-geoclue2 -l pl.UTF-8
Interfejs języka Vala do biblioteki geoclue2.

%prep
%setup -q -n geoclue-%{version}

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-demo-agent \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-systemdsystemunitdir=%{systemdunitdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgeoclue-2.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_libexecdir}/geoclue
%dir %{_sysconfdir}/geoclue
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/geoclue/geoclue.conf
%{systemdunitdir}/geoclue.service
/etc/dbus-1/system.d/org.freedesktop.GeoClue2.conf
/etc/dbus-1/system.d/org.freedesktop.GeoClue2.Agent.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.GeoClue2.service
# demos
/etc/xdg/autostart/geoclue-demo-agent.desktop
%dir %{_libexecdir}/geoclue-2.0
%dir %{_libexecdir}/geoclue-2.0/demos
%attr(755,root,root) %{_libexecdir}/geoclue-2.0/demos/agent
%attr(755,root,root) %{_libexecdir}/geoclue-2.0/demos/where-am-i
%{_desktopdir}/geoclue-demo-agent.desktop
%{_desktopdir}/geoclue-where-am-i.desktop

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
