Summary:	A modular geoinformation service
Summary(pl.UTF-8):	Modularna usługa geoinformacyjna
Name:		geoclue2
Version:	2.1.8
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	http://www.freedesktop.org/software/geoclue/releases/2.1/geoclue-%{version}.tar.xz
# Source0-md5:	49096b9c3c2458b5e8e36b886983d9aa
URL:		http://geoclue.freedesktop.org/
BuildRequires:	ModemManager-devel >= 1.0.0
BuildRequires:	NetworkManager-devel >= 0.9.8.0
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.34.0
BuildRequires:	gnome-common
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	json-glib-devel >= 0.14
BuildRequires:	libnotify-devel
BuildRequires:	libsoup-devel >= 2.4.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libxml2-devel >= 1:2.7
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	yelp-tools
Requires:	dbus
Requires:	glib2 >= 1:2.34.0
Requires:	json-glib >= 0.14
Requires:	libsoup >= 2.4.0
Requires:	libxml2 >= 1:2.7
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

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-demo-agent \
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
%attr(755,root,root) %{_libexecdir}/geoclue
%dir %{_sysconfdir}/geoclue
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/geoclue/geoclue.conf
%{systemdunitdir}/geoclue.service
/etc/dbus-1/system.d/org.freedesktop.GeoClue2.conf
/etc/dbus-1/system.d/org.freedesktop.GeoClue2.Agent.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.GeoClue2.service
# demos
%dir %{_libexecdir}/geoclue-2.0
%dir %{_libexecdir}/geoclue-2.0/demos
%attr(755,root,root) %{_libexecdir}/geoclue-2.0/demos/agent
%attr(755,root,root) %{_libexecdir}/geoclue-2.0/demos/where-am-i
%{_desktopdir}/geoclue-demo-agent.desktop
%{_desktopdir}/geoclue-where-am-i.desktop

%files devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/geoclue-2.0.pc
%{_datadir}/dbus-1/interfaces/org.freedesktop.GeoClue2.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.GeoClue2.Agent.xml
