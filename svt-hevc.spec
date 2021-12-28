%define major 1
%define libpackage %mklibname svt-hevc %{major}
%define devpackage %mklibname -d svt-hevc

%define oname   SVT-HEVC

Name:           svt-hevc
Version:        1.5.1
Release:        1
Summary:        Scalable Video Technology for AV1 Encoder
Group:          System/Libraries
License:        BSD-2-Clause-Patent
URL:            https://github.com/OpenVisualCloud/SVT-HEVC/
Source0:        https://github.com/OpenVisualCloud/SVT-HEVC/archive/v%{version}/%{oname}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  meson
BuildRequires:  yasm
BuildRequires:  help2man
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)

Requires:	%{libpackage} = %{EVRD}
Requires: gstreamer1.0-%{name} = %{EVRD}

%description
The Scalable Video Technology for hevc Encoder (SVT-hevc Encoder) is an
hevc-compliant encoder library core. The SVT-AV1 development is a
work-in-progress targeting performance levels applicable to both VOD and Live
encoding / transcoding video applications.

%package -n %{libpackage}
Summary:    SVT-hevc libraries
Group:		System/Libraries

%description -n %{libpackage}
This package contains SVT-hevc libraries.

%package -n %{devpackage}
Summary:    Development files for SVT-hevc
Requires:	%{name} = %{EVRD}
Requires:	%{libpackage} = %{EVRD}
Recommends: %{name}-devel-docs = %{EVRD}

%description -n %{devpackage}
This package contains the development files for SVT-hevc.

%package -n     gstreamer1.0-%{name}
Summary:        GStreamer 1.0 %{name}-based plug-in
Requires:       gstreamer1.0-plugins-base

%description -n gstreamer1.0-%{name}
This package provides %{name}-based GStreamer plug-in.

%prep
%autosetup -p1 -n %{oname}-%{version}
# Patch build gstreamer plugin
#sed -e "s|install: true,|install: true, include_directories : [ include_directories('../Source/API') ], link_args : '-lSvtAv1Enc',|" \
#-e "/svtav1enc_dep =/d" -e 's|, svtav1enc_dep||' -e "s|svtav1enc_dep.found()|true|" -i gstreamer-plugin/meson.build

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release
%make_build

cd ..
export LIBRARY_PATH="$LIBRARY_PATH:$(pwd)/Bin/Release"
cd gstreamer-plugin
%meson
%meson_build
cd ..

%install
%make_install -C build
rm -f %{buildroot}%{_libdir}/*.{a,la}

pushd gstreamer-plugin
%meson_install
popd

%files
%{_bindir}/SvtHevcEncApp

%files -n %{libpackage}
%license LICENSE.md
%doc README.md Docs/svt-hevc_encoder_user_guide.md
%{_libdir}/libSvtHevcEnc.so.%{major}*

%files -n %{devpackage}
%{_includedir}/%{name}
%{_libdir}/libSvtHevcEnc.so
%{_libdir}/pkgconfig/*.pc


%files -n gstreamer1.0-%{name}
%{_libdir}/gstreamer-1.0/libgstsvtav1enc.so
