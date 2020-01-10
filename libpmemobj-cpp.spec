%global min_libpmemobj_ver 1.4
%global upstreamversion 1.5

Name:		libpmemobj-cpp
Version:	1.5
Release:	1%{?dist}
Summary:	C++ bindings for libpmemobj
# Note: tests/external/libcxx is dual licensed using University of Illinois "BSD-Like" license and the MIT license. It's used only during development/testing and is NOT part of the binary RPM.
License:	BSD
URL:		http://pmem.io/pmdk/cpp_obj/

Source0:	https://github.com/pmem/%{name}/archive/%{upstreamversion}.tar.gz#/%{name}-%{upstreamversion}.tar.gz

Patch0:		libpmemobj-cpp-cmake-2.8.patch

BuildRequires:	libpmemobj-devel >= %{min_libpmemobj_ver}
BuildRequires:	cmake >= 2.8
BuildRequires:	glibc-devel
BuildRequires:	pkgconfig
BuildRequires:	doxygen
BuildRequires:	perl-Encode
BuildRequires:	devtoolset-7-gcc
BuildRequires:	devtoolset-7-gcc-c++
BuildRequires:	devtoolset-7-build

# There's nothing x86-64 specific in this package, but we have
# to duplicate what spec for pmdk/libpmemobj has at the moment.
# Relevant bug reports:
# https://bugzilla.redhat.com/show_bug.cgi?id=1340634
# https://bugzilla.redhat.com/show_bug.cgi?id=1340635
# https://bugzilla.redhat.com/show_bug.cgi?id=1340636
# https://bugzilla.redhat.com/show_bug.cgi?id=1340637
ExclusiveArch: x86_64

%description
This package contains header files for libpmemobj C++ bindings and C++
containers built on top of them.

# Specify a virtual Provide for libpmemobj++-static package, so the package
# usage can be tracked.
%package -n libpmemobj++-devel
Summary: C++ bindings for Persistent Memory Transactional Object Store library
Provides: libpmemobj++-static = %{version}-%{release}
Requires: libpmemobj-devel >= %{min_libpmemobj_ver}

%description -n libpmemobj++-devel
This package contains header files for libpmemobj C++ bindings and C++
containers built on top of them.

The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming.

%files -n libpmemobj++-devel
%{_libdir}/pkgconfig/libpmemobj++.pc
%dir %{_includedir}/libpmemobj++
%{_includedir}/libpmemobj++/*.hpp
%dir %{_includedir}/libpmemobj++/detail
%{_includedir}/libpmemobj++/detail/*.hpp
%dir %{_includedir}/libpmemobj++/experimental
%{_includedir}/libpmemobj++/experimental/*.hpp
%dir %{_libdir}/libpmemobj++
%dir %{_libdir}/libpmemobj++/cmake
%{_libdir}/libpmemobj++/cmake/libpmemobj++-config-version.cmake
%{_libdir}/libpmemobj++/cmake/libpmemobj++-config.cmake

%license LICENSE

%doc ChangeLog README.md

%package -n libpmemobj++-doc
Summary: HTML documentation for libpmemobj++

%description -n libpmemobj++-doc
HTML documentation for libpmemobj++.

%files -n libpmemobj++-doc
%dir %{_docdir}/libpmemobj++
%{_docdir}/libpmemobj++/*

%license LICENSE

%doc ChangeLog README.md

%global debug_package %{nil}

%prep
%setup -q
%patch0 -p1 -b .orig

%build

# Enable Developer Tool Set (DTS)
%if 0%{?rhel} == 7
source /opt/rh/devtoolset-7/enable
%endif

mkdir build
cd build
%cmake .. -DCMAKE_INSTALL_DOCDIR=%{_docdir}/libpmemobj++
%make_build

%install
cd build
%make_install

%check
cd build
ctest -V %{?_smp_mflags}

%changelog
* Fri Apr 05 2019 Jeff Moyer <jmoyer@redhat.com - 1.5-1.el7
- initial import for rhel7
- Related: bz#1659664

* Thu Nov 8 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.5-1
- Initial RPM release
