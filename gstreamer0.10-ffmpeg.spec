%define bname gstreamer0.10
%define name %bname-ffmpeg
%define oname gst-ffmpeg
%define version 0.10.2
%define release %mkrel 1
%define gstver %version

Summary: Gstreamer plugin for the ffmpeg codec
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://gstreamer.freedesktop.org/src/gst-ffmpeg/%{oname}-%{version}.tar.bz2
License: GPL
Group: Video
Url: http://www.gstreamer.net
BuildRequires: libgstreamer-plugins-base-devel >= %gstver
BuildRequires: liboil-devel
BuildRequires: libcheck-devel valgrind
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Video codec plugin for GStreamer based on the ffmpeg libraries.

%prep
%setup -q -n %oname-%version

%build
%configure2_5x
%make

%check
cd tests/check
#gw fails in iurt
#make check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
rm -f %buildroot%_libdir/gstreamer*/*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README NEWS TODO ChangeLog AUTHORS docs/plugins/html/
%_libdir/gstreamer-*/libgstffmpeg.so
%_libdir/gstreamer-*/libgstpostproc.so


