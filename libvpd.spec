## SLES
%if 0%{?suse_version}
%define name	libvpd2
%define sql	sqlite3-devel
%endif

## RHEL
%if 0%{?rhel_version}
%define name	libvpd
%define sql	sqlite-devel
%endif

%define version 2.2.4

Name:		%{name}
Version:	%{version}
Release:	1%{?dist}
Summary:	VPD Database access library for lsvpd

Group:		System Environment/Libraries
License:	LGPLv2+
Vendor:         IBM Corp.
URL:		http://linux-diag.sf.net/lsvpd.html
Source:		http://downloads.sourceforge.net/linux-diag/libvpd/%{version}/libvpd-%{version}.tar.gz

#SLES
%if 0%{?suse_version}
Source2:	baselibs.conf
Patch1:		libvpd2.makefile.patch
%endif

## RHEL
%if 0%{?rhel_version}
# RHEL >= .
%if 0%{?rhel_version} == 700
ExclusiveArch: ppc ppc64
%endif
%if 0%{?rhel_version} >= 700
Obsoletes: libvpd(ppc)
ExclusiveArch: ppc64 ppc64le
%endif
%else
ExclusiveArch: ppc64 ppc64le
%endif


BuildRequires:	zlib-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	automake
BuildRequires:	pkgconfig
BuildRequires:	%{sql}
BuildRequires:	autoconf
BuildRequires:	udev
BuildRequires:	gcc-c++

%description
The libvpd package contains the classes that are used to access a vpd database
created by vpdupdate in the lsvpd package.

%package devel
Summary:	Header files for libvpd
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{sql}

%description devel
Contains header files for building with libvpd.

%prep
%setup -q -n libvpd-%{version}
%if 0%{?suse_version}
%patch1 -p1
%endif

%if 0%{?suse_version}
autoreconf -fvi
%endif

%build
./bootstrap.sh
%configure --disable-static
%{__make} %{?_smp_mflags}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%exclude %{_libdir}/*.la
%{_libdir}/*.so.*
%if 0%{?suse_version}
/%{_udevrulesdir}/90-vpdupdate.rules
%dir %{_localstatedir}/lib/lsvpd
%{_localstatedir}/lib/lsvpd/run.vpdupdate
%endif
%if 0%{?rhel_version}
%{_sysconfdir}/udev/rules.d/90-vpdupdate.rules
%{_sharedstatedir}/lsvpd/run.vpdupdate
%endif

%files devel
%defattr(-,root,root,-)
%exclude %{_libdir}/*.la
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog

* Thu Aug 14 2014 Vasant Hegde <hegdevasant@linux.vnet.ibm.com> 2.2.4
- Cleanup build tools
- Shift configure.in to configure.ac
- Remove out dated debian directory

* Thu Mar 13 2014 Suzuki K Poulose <suzuki@in.ibm.com> 2.2.3
- Relese version 2.2.3

* Tue Nov 5 2013 Suzuki K Poulose <suzuki@in.ibm.com> 2.2.2-0
- Release version 2.2.2

* Thu Oct 31 2013 Phani Yadav <phayadav@linux.vnet.ibm.com>
- Automation of vpdupdate

* Wed Feb 20 2013 Harsh P Bora <harsh@linux.vnet.ibm.com> 2.2.1-1
- Added Vendor tag in RPM package.

* Fri Jan 18 2013 Harsh P Bora <harsh@linux.vnet.ibm.com> 2.2.1-0
- Fixed a possible segfault when fetching a corrupt vpd database

* Fri Dec 4 2009 Jim Keniston <jkenisto@us.ibm.com> 2.1.2-0
- Fixed a pack/unpack mismatch that was introduced with N5/N6 support.
For every Component, all 28 DataItems between sysFsNode and plantMfg
were getting the wrong values.

* Mon Mar 17 2008 Eric Munson <ebmunson@us.ibm.com> 2.0.1-1
- Update for libvpd-2.0.1

* Tue Feb 26 2008 Eric Munson <ebmunson@us.ibm.com> 2.0.0-2
- Updating release number for new build in FC

* Mon Feb 25 2008 Eric Munson <ebmunson@us.ibm.com> 2.0.0-1
- Updated library to use sqlite instead of berkeley db.

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5.0-2
- Autorebuild for GCC 4.3

* Mon Jan 7 2008 Eric Munson <ebmunson@us.ibm.com> -1.5.0-1
- Moved pkgconfig to devel Requires
- Updated %%defattrs to -,root,root,-
- Added AUTHORS to %%doc

* Thu Jan 3 2008 Eric Munson <ebmunson@us.ibm.com> - 1.5.0-0
- Updated Requires and Provides fields per fedora community request

* Fri Dec 7 2007 Brad Peters <bpeters@us.ibm.com> - 1.4.2-0
- Added functions to helper_functions class
- Mnior changes necessary to support new device discovery method

* Fri Nov 16 2007 Eric Munson <ebmunson@us.ibm.com> - 1.4.1-1
- Removing INSTALL from docs and docs from -devel package
- Fixing Makfile.am so libraries have the .so extension
- Using %%configure, %%{__make}, and %%{__rm} calls
- Changing source URL

* Wed Oct 31 2007 Eric Munson <ebmunson@us.ibm.com> - 1.4.0-2
- Changing files lists for libdirs to match library file names

* Tue Oct 30 2007 Eric Munson <ebmunson@us.ibm.com> - 1.4.0-1
- Adding C Library to files lists.

* Sat Oct 20 2007 Ralf Corsepius <rc040203@freenet.de>	- 1.3.5-4
- Various spec-file fixes.

* Fri Oct 19 2007 Eric Munson <ebmunson@us.ibm.com> - 1.3.5-3
- Removed hard coded /usr/lib from spec file
- Install now sets all headers to 644
- Updated license
