#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	C++ implementation of the OpenTracing API
Summary(pl.UTF-8):	Implementacja C++ API OpenTracing
Name:		opentracing-cpp
Version:	1.6.0
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/opentracing/opentracing-cpp/releases
Source0:	https://github.com/opentracing/opentracing-cpp/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	484fed46980b9ec02aac44e4a37adeda
URL:		https://opentracing.io/
BuildRequires:	cmake >= 3.1
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C++ implementation of the OpenTracing API <https://opentracing.io/>.

%description -l pl.UTF-8
Implementacja C++ API OpenTracing <https://opentracing.io/>.

%package devel
Summary:	Header files for OpenTracing libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek OpenTracing
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7

%description devel
Header files for OpenTracing libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek OpenTracing.

%package static
Summary:	Static OpenTracing libraries
Summary(pl.UTF-8):	Statyczne biblioteki OpenTracing
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenTracing libraries.

%description static -l pl.UTF-8
Statyczne biblioteki OpenTracing.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	%{!?with_static_libs:-DBUILD_STATIC_LIBS=OFF} \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DENABLE_LINTING=OFF \
	-DLIB_INSTALL_DIR=%{_lib}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_libdir}/libopentracing.so.*.*.*
%ghost %{_libdir}/libopentracing.so.1
%attr(755,root,root) %{_libdir}/libopentracing_mocktracer.so.*.*.*
%ghost %{_libdir}/libopentracing_mocktracer.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/libopentracing.so
%{_libdir}/libopentracing_mocktracer.so
%{_includedir}/opentracing
%{_libdir}/cmake/OpenTracing

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libopentracing.a
%{_libdir}/libopentracing_mocktracer.a
%endif
