%define name libservicelog
%define version 1.1.15

%if 0%{?suse_version}
%define sql	sqlite3-devel
%endif

## RHEL
%if 0%{?rhel_version}
%define sql	sqlite-devel
%endif

Name:           %{name}
%if 0%{?suse_version}
%define lname libservicelog-1_1-1
%endif
Version:        %{version}
Release:        1%{?dist}
Summary:        Servicelog Database and Library
%if 0%{?suse_version}
License:	GPL-2.0+
Group:          System/Libraries
%endif
%if 0%{?rhel_version}
Group:          System Environment/Libraries
License:        LGPLv2
%endif
Vendor:		IBM Corp.
URL:            http://linux-diag.sourceforge.net/libservicelog
Source0:        http://downloads.sourceforge.net/linux-diag/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:        baselibs.conf
Source2:        libservicelog-rpmlintrc
BuildRequires:	gcc-c++
BuildRequires:	bison
BuildRequires:  %{sql}
BuildRequires:	flex
BuildRequires:	librtas-devel
BuildRequires:	pkgconfig
BuildRequires:	libtool
BuildRequires:	automake
BuildRequires:	glibc-devel
Requires(pre):	/usr/sbin/groupadd

%if 0%{?rhel_version}
Patch0:	libservicelog-1.1.15-libs.patch
%endif

%description
The libservicelog package contains a library to create and maintain a
database for storing events related to system service. This database
allows for the logging of serviceable and informational events, and for
the logging of service procedures that have been performed upon the
system.

%if 0%{?suse_version}
%package -n %lname
Summary:        Servicelog Database and Library
Group:          System/Libraries
Requires:       %name

%description -n %lname
The libservicelog package contains a library to create and maintain a
database for storing events related to system service. This database
allows for the logging of serviceable and informational events, and for
the logging of service procedures that have been performed upon the
system.
%endif

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
%if 0%{?suse_version}
Requires:       %lname = %version
%endif
%if 0%{?rhel_version}
Requires:       %{name} = %{version}-%{release}
%endif

%description    devel
Contains header files for building with libservicelog.

%prep
%setup -q
%if 0%{?rhel_version}
%patch0 -p1
%endif

%build
./bootstrap.sh
%configure --disable-static
%{__make} %{?_smp_mflags}

%install
touch servicelog.db
install -D --mode=754 servicelog.db \
	$RPM_BUILD_ROOT/var/lib/servicelog/servicelog.db
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group service >/dev/null || /usr/sbin/groupadd service

%if 0%{?suse_version}
%post -n %lname -p /sbin/ldconfig
%postun -n %lname -p /sbin/ldconfig
%endif

%if 0%{?rhel_version}
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS README
%exclude %{_libdir}/*.la
%if 0%{?rhel_version}
%{_libdir}/lib*.so.*
%endif
%attr( 754, root, service ) %dir /var/lib/servicelog
%config(noreplace) %verify(not md5 size mtime) %attr(644,root,service) /var/lib/servicelog/servicelog.db

%if 0%{?suse_version}
%files -n %lname
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*
%endif

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/servicelog-1
%{_libdir}/*.la
%{_libdir}/pkgconfig/servicelog-1.pc

%changelog
* Thu Aug 14 2014 Vasant Hegde <hegdevasant at linux.vnet.ibm.com> 1.1.15
- Cleanup build tools (configure.ac and Makefile.am)

* Tue Aug 20 2013 Vasant Hegde <hegdevasant at linux.vnet.ibm.com> 1.1.14
- Include servicelog.db and bootstrap.sh file into compression file list

* Thu Jan 10 2013 Vasant Hegde <hegdevasant at linux.vnet.ibm.com> 1.1.13
- Legalize SQL insert command input string
- repair_action : fix output format issue
- Minor typo fix

* Wed Sep 12 2012 Vasant Hegde <hegdevasant at linux.vnet.ibm.com> 1.1.12
- Minor changes

* Sat Nov 07 2009 Jim Keniston <jkenisto at us.ibm.com>, Brad Peters 1.1.x
- Minor changes continued in the ensuing months

* Sat Aug 16 2008 Mike Strosaker <strosake at austin.ibm.com> 1.0.1
- Create /var/lib/servicelog/servicelog.db at install time
- Additional comments and code cleanup
- Fix issue with notification tools not being started
- Beautify printing of notification tools

* Tue Mar 04 2008 Mike Strosaker <strosake at austin.ibm.com> 1.0.0
- Initial creation of the package
