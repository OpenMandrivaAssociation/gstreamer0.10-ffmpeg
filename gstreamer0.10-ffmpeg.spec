%define _disable_ld_no_undefined 1
%define	api	0.10
%define	bname	gstreamer%{api}
%define	oname	gst-ffmpeg

# _with = default off, _without = default on
%bcond_with external_ffmpeg

Name:		%{bname}-ffmpeg
Version:	0.10.13
Release:	14
License:	GPLv2+
Group:		Video
Url:		https://www.gstreamer.net
Source0:	http://gstreamer.freedesktop.org/src/gst-ffmpeg/%{oname}-%{version}.tar.bz2
# (Anssi 01/2008) Enable mpegts demuxer as well, for now.
# If either
# https://core.fluendo.com/gstreamer/trac/ticket/88 or
# http://bugzilla.gnome.org/show_bug.cgi?id=347342
# will be fixed, we should probably remove this patch and package the
# "native" non-ffmpeg MPL-licensed fluendo-mpegdemux, which is apparently
# highly preferred to ffmpeg plugin by upstream.
Patch0:		gst-ffmpeg-enable-mpegts.patch
Patch1:		gst-ffmpeg-fix-format-strings.patch
Patch2:		gst-ffmpeg-0.10.13-gcc-4.7-1.patch
Patch3: gst-ffmpeg-0.10.13-ffmpeg-1.0.patch
Patch4:	gst-ffmpeg-0.10.13-planar-audio.patch
Patch5: gst-ffmpeg-0.10.13-ffmpeg-2.0.patch
Patch6: gst-ffmpeg-0.10.13-ffmpeg-2.4.patch

BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gstreamer-plugins-base-%{api})
BuildRequires:	pkgconfig(orc-0.4)
BuildRequires:	yasm
%ifnarch %{arm} %{mips}
BuildRequires:	valgrind
%endif
%if %with external_ffmpeg
BuildRequires:	ffmpeg-devel
%endif

%description
Video codec plugin for GStreamer based on the ffmpeg libraries.

%prep
%setup -qn %{oname}-%{version}
%autopatch -p1

%build
# gst-ffmpeg mp3 decoder has issues (eg no seeking support), disable it since
# gst-plugins-bad and gst-fluendo both ship better mp3 decoders
%configure2_5x \
	--disable-static \
	--with-package-name='%{distribution} %{name} package' \
	--with-package-origin='%{disturl}' \
	--with-ffmpeg-extra-configure='--disable-decoder=mp3 \
	--disable-decoder=mp3on4 \
	--disable-decoder=mp3adu \
	--disable-demuxer=mp3 \
	--disable-demuxer=asf' \
%if %with external_ffmpeg
	--with-system-ffmpeg
%endif

%make

%install
%makeinstall_std

%files
%doc README NEWS TODO ChangeLog AUTHORS
%{_libdir}/gstreamer-%{api}/libgstffmpeg.so
%{_libdir}/gstreamer-%{api}/libgstffmpegscale.so
%{_libdir}/gstreamer-%{api}/libgstpostproc.so

