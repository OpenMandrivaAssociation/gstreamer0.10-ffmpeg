%define bname gstreamer0.10
%define name %bname-ffmpeg
%define oname gst-ffmpeg
%define version 0.10.3
%define release %mkrel 3
%define gstver %version

Summary: Gstreamer plugin for the ffmpeg codec
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://gstreamer.freedesktop.org/src/gst-ffmpeg/%{oname}-%{version}.tar.bz2
# (Anssi 01/2008) Enable mpegts demuxer as well, for now.
# If either
# https://core.fluendo.com/gstreamer/trac/ticket/88 or
# http://bugzilla.gnome.org/show_bug.cgi?id=347342
# will be fixed, we should probably remove this patch and package the
# "native" non-ffmpeg MPL-licensed fluendo-mpegdemux, which is apparently
# highly preferred to ffmpeg plugin by upstream.
Patch0: gst-ffmpeg-enable-mpegts.patch
License: GPLv2+
Group: Video
URL: http://www.gstreamer.net
BuildRequires: libgstreamer-plugins-base-devel >= %gstver
BuildRequires: liboil-devel
BuildRequires: freetype2-devel
BuildRequires: libcheck-devel valgrind
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Video codec plugin for GStreamer based on the ffmpeg libraries.

%prep
%setup -q -n %oname-%version
%patch0 -p1

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

