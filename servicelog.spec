%define name servicelog
%define version 1.1.13

%if 0%{?suse_version}
%define sql	sqlite3-devel
%endif

## RHEL
%if 0%{?rhel_version}
%define sql	sqlite-devel
%endif

Name:           %{name}
Version:        %{version}
Release:        1%{?dist}
Summary:        Servicelog Tools

Group:          System Environment/Base
%if 0%{?suse_version}
License:	GPL-2.0
%endif
%if 0%{?rhel_version}
License:        GPLv2
%endif
Vendor:		IBM Corp.
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
URL:            http://linux-diag.sourceforge.net/servicelog
Source0:        http://downloads.sourceforge.net/linux-diag/%{name}/%{version}/%{name}-%{version}.tar.gz

BuildRequires:	librtas-devel
BuildRequires:  %{sql}
BuildRequires:  libservicelog-devel
BuildRequires:	libtool
BuildRequires:	automake
ExclusiveArch:	ppc ppc64 ppc64le

%description
Command-line interfaces for viewing and manipulating the contents of
the servicelog database. Servicelog contains entries that are useful
for performing system service operations, and for providing a history
of service operations that have been performed on the system.

%files
%defattr(-,root,root,-)
%doc COPYING README
%attr ( 744, root,root ) %{_bindir}/*
%attr ( 744, root,root ) %{_sbindir}/slog_common_event
%{_mandir}/man8/*.8*

%prep
%setup -q
./bootstrap.sh

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%changelog
* Thu Aug 14 2014  Vasant Hegde <hegdevasant at linux.vnet.ibm.com> 1.1.13
- Grant permission to link with librtas library
- Fixed couple of issues in build tool

* Fri Mar 07 2014 Vasant Hegde <hegdevasant at linux.vnet.ibm.com> 1.1.12
- Added platform validation

* Tue Jan 29 2013 Vasant Hegde <hegdevasant at linux.vnet.ibm.com> 1.1.11-3
- log_repair_action : usage message format fix

* Thu Jan 10 2013 Vasant Hegde <hegdevasant at linux.vnet.ibm.com> 1.1.11-2
- servicelog_notify : validate command line arguments
- Minor fix to man pages
- Spec file cleanup

* Wed Sep 12 2012 Vasant Hegde <hegdevasant at linux.vnet.ibm.com> 1.1.11
- servicelog_manage : resurrecting the --clean option

* Fri Sep 7 2012 Vasant Hegde <hegdevasant at linux.vnet.ibm.com> 1.1.11
- Minor changes

* Mon Feb 13 2012 Jim Keniston <jkenisto at us.ibm.com> 1.1.10
- Resurrected servicelog_manage(8) man page (LTC bugzilla #70852).
- Major fixups to the other man pages (#70853) and to servicelog_notify.

* Mon Mar 28 2011 Jim Keniston <jkenisto at us.ibm.com> 1.1.9
- Fixed servicelog_manage bugs (LTC bugzilla #70459).

* Wed Oct 20 2010 Brad Peters 1.1.8
- Minor changes

* Sat Nov 07 2009 Jim Keniston <jkenisto at us.ibm.com>, Brad Peters 1.1.x
- Added backward compatibility with [lib]servicelog v0.2.9.

* Mon Aug 18 2008 Mike Strosaker <strosake at austin.ibm.com> 1.0.1
- Various small fixes to the servicelog_notify command

* Tue Mar 04 2008 Mike Strosaker <strosake at austin.ibm.com> 1.0.0
- Initial creation of the package
