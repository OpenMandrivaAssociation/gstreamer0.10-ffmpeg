%define bname gstreamer0.10
%define name %bname-ffmpeg
%define oname gst-ffmpeg
%define version 0.10.4
%define release %mkrel 2
%define gstver %version

# _with = default off, _without = default on
%bcond_with external_ffmpeg

# (Anssi 01/2008) External ffmpeg disabled because of issues:
# with FLV file with totem:
# ** ERROR:(gstffmpegdec.c:731):gst_ffmpegdec_get_buffer: code should not be reached
# with VDR stream as per manual pipeline in http://bugzilla.gnome.org/show_bug.cgi?id=506902 :
# (gst-launch-0.10:23590): GStreamer-CRITICAL **: gst_value_set_fraction: assertion `denominator != 0' failed
# No playback in either case.

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
%if %with external_ffmpeg
BuildRequires: ffmpeg-devel
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Video codec plugin for GStreamer based on the ffmpeg libraries.

%prep
%setup -q -n %oname-%version
%patch0 -p1 -b .mpegts

%build
%configure2_5x \
  --with-package-name='Mandriva %name package' \
  --with-package-origin='http://www.mandriva.com/' \
%if %with external_ffmpeg
	--with-system-ffmpeg
%endif

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

