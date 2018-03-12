#ciscosafec version we are going to release
%define ciscosafec_version %(cat %{_topdir}/build.properties | grep ^VERSION | awk -F'[=]' '{print $2}')

#get major minor and micro from version
%define major %( echo %{ciscosafec_version} | cut -d '.' -f 1 )
%define minor %( echo %{ciscosafec_version} | cut -d '.' -f 2 )
%define micro %( echo %{ciscosafec_version} | cut -d '.' -f 3 )

#The version release number
%define release_number %(cat %{_topdir}/build.properties | grep ^RELEASE | awk -F'[=]' '{print $2}')

#The epoch number
%define epoch_number %(cat %{_topdir}/build.properties | grep ^EPOCH | awk -F'[=]' '{print $2}')

%global _performance_build 1

Summary: To help enforce better C programming practices
Name: safec
Version: %{ciscosafec_version}
Release: %{release_number}%{?dist}
Epoch: %{epoch_number}
Source: ciscosafec-%{ciscosafec_version}.tar.gz
License: SafeC
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

# Build changes
Patch1: safec-4.0.37-i686tests.patch

%description
A C Library that utilizes checks for to help protect against runtime violatons

%package libs
Summary: A C Library that utilizes checks for to help protect against runtime violatons
Group: System Environment/Libraries
Provides: ciscosafec = %{ciscosafec_version}

%description libs
A C Library that utilizes checks for to help protect against runtime violatons.

%prep
##################### untar to ciscosafec
%setup -q -n ciscosafec-%{ciscosafec_version}

%patch1 -p1 -b .i686tests

sed -i "s/m4_define(\[safec_major_version\], \[4\])/m4_define(\[safec_major_version\], \[%{major}\])/" configure.ac
sed -i "s/m4_define(\[safec_minor_version\], \[1\])/m4_define(\[safec_minor_version\], \[%{minor}\])/" configure.ac
sed -i "s/m4_define(\[safec_micro_version\], \[0\])/m4_define(\[safec_micro_version\], \[%{micro}\])/" configure.ac
sed -i 's/\[safec_major_version.safec_minor_version.safec_micro_version-dev\]/\[safec_major_version.safec_minor_version.safec_micro_version\]/' configure.ac

%build
# Figure out which flags we want to use.
# default
sslarch=%{_os}-%{_target_cpu}
%ifarch %ix86
sslarch=linux-elf
if echo %{_target} | grep -q i686 ; then
  export CFLAGS="-DLINUX32 -m32"
	export  CXXFLAGS="-m32"
	export  LDFLAGS="-m32"
	safecflags="--build=i686-pc-linux-gnu"
fi
%endif
%ifarch x86_64
safecflags=""
%endif
autoreconf
./configure --includedir=/usr/include/safec --libdir=%{_libdir} \
  ${safecflags}  --with-cunit-dir=/usr/share/CUnit\
  --enable-perf --enable-gcov

make -j16
make dist
make hash


%check
# Verify that what was compiled actually works.
pushd test
./ciscosafec_runtest -xml
./ciscosafec_runtest-dynamic -xml
popd


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files libs
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/libciscosafec.so.%{major}.0.%{minor}
%attr(0755,root,root) %{_libdir}/libciscosafec.so.%{major}
%attr(0755,root,root) %{_libdir}/libciscosafec.so
%attr(0755,root,root) %{_libdir}/libciscosafec.la
%attr(0755,root,root) %{_libdir}/libciscosafec.a
%{_prefix}/include/safec

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig
