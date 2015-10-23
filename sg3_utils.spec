%global rescan_script rescan-scsi-bus.sh

Summary: Utilities for devices that use SCSI command sets
Name: sg3_utils
Version: 1.37
Release: 5%{?dist}
License: GPLv2+ and BSD
Group: Applications/System
Source0: http://sg.danny.cz/sg/p/sg3_utils-%{version}.tgz
Source1: rescan-scsi-bus.sh.8
Source2: scsi-rescan.8
# https://bugzilla.redhat.com/show_bug.cgi?id=920687
Patch0: sg3_utils-1.37-dont-open-dev-snapshot.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=948463
Patch1: sg3_utils-1.37-man-pages-fix.patch
URL: http://sg.danny.cz/sg/sg3_utils.html
Requires: %{name}-libs = %{version}-%{release}


%description
Collection of Linux utilities for devices that use the SCSI command set.
Includes utilities to copy data based on "dd" syntax and semantics (called
sg_dd, sgp_dd and sgm_dd); check INQUIRY data and VPD pages (sg_inq); check
mode and log pages (sginfo, sg_modes and sg_logs); spin up and down
disks (sg_start); do self tests (sg_senddiag); and various other functions.
See the README, CHANGELOG and COVERAGE files. Requires the linux kernel 2.4
series or later. In the 2.4 series SCSI generic device names (e.g. /dev/sg0)
must be used. In the 2.6 series other device names may be used as
well (e.g. /dev/sda).

Warning: Some of these tools access the internals of your system
and the incorrect usage of them may render your system inoperable.

%package libs
Summary: Shared library for %{name}
Group: System Environment/Libraries

%description libs
This package contains the shared library for %{name}.

%package devel
Summary: Development library and header files for the sg3_utils library
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: glibc-headers

%description devel
This package contains the %{name} library and its header files for
developing applications.

%prep
%setup -q
%patch0 -p1 -b .dev-snapshot
%patch1 -p1 -b .man-fixes


%build
%configure --disable-static

# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la

install -p -m 755 scripts/%{rescan_script} $RPM_BUILD_ROOT%{_bindir}
( cd $RPM_BUILD_ROOT%{_bindir}; ln -sf %{rescan_script} scsi-rescan )

install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man8


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%doc AUTHORS BSD_LICENSE COPYING COVERAGE CREDITS ChangeLog README README.sg_start
%{_bindir}/*
%{_mandir}/man8/*

%files libs
%doc BSD_LICENSE COPYING
%{_libdir}/*.so.*

%files devel
%{_includedir}/scsi/*.h
%{_libdir}/*.so


%changelog
* Wed Jan 29 2014 Dan Horák <dan@danny.cz> - 1.37-5
- fix various man pages (#948463)
- add man page for the rescan-scsi-bus.sh script (#948463)
- Resolves: #948463

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.37-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.37-3
- Mass rebuild 2013-12-27

* Fri Oct 18 2013 Dan Horák <dan@danny.cz> - 1.37-2
- include fix for #920687

* Wed Oct 16 2013 Dan Horák <dan@danny.cz> - 1.37-1
- update to version 1.37
- switch to included rescan-scsi-bus script

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 06 2013 Dan Horák <dan@danny.cz> - 1.36-1
- update to version 1.36
- modernize spec

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Dan Horák <dan@danny.cz> - 1.35-1
- update to version 1.35

* Thu Oct 18 2012 Dan Horák <dan@danny.cz> - 1.34-1
- update to version 1.34

* Fri Sep 14 2012 Dan Horák <dan@danny.cz> - 1.33-4
- add fix for sg3_utils >= 1.32 to the rescan-scsi-bus script

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr  4 2012 Dan Horák <dan@danny.cz> - 1.33-2
- include rescan-scsi-bus script 1.56

* Tue Apr  3 2012 Dan Horák <dan@danny.cz> - 1.33-1
- update to version 1.33

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Feb 18 2011 Dan Horák <dan@danny.cz> - 1.31-1
- update to version 1.31

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul  8 2010 Dan Horák <dan@danny.cz> - 1.29-2
- added license texts into -libs subpackage

* Mon Apr 12 2010 Dan Horák <dan@danny.cz> - 1.29-1
- update to version 1.29

* Thu Jan 14 2010 Dan Horák <dan@danny.cz> - 1.28-2
- include rescan-scsi-bus script 1.35
- rebase patches and add fix for issue mentioned in #538787

* Thu Oct 22 2009 Dan Horák <dan@danny.cz> - 1.28-1
- update to version 1.28
- added fixes from RHEL to rescan-scsi-bus.sh
- added scsi-rescan symlink to the rescan-scsi-bus.sh script

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 28 2009 Dan Horák <dan@danny.cz> - 1.27-1
- update to version 1.27
- changelog: http://sg.danny.cz/sg/p/sg3_utils.ChangeLog

* Tue Mar 31 2009 Dan Horák <dan@danny.cz> - 1.26-4
- add dependency between the libs subpackage and the main package (#492921)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov  3 2008 Dan Horák <dan@danny.cz> - 1.26-2
- update URL
- include rescan-scsi-bus script 1.29

* Mon Jun 30 2008 Dan Horák <dan@danny.cz> - 1.26-1
- update to upstream version 1.26

* Fri Mar 28 2008 Phil Knirsch <pknirsch@redhat.com> - 1.25-4
- Dropped really unnecessary Provides of sg_utils (#226414)
- Use --disable-static in configure (#226414)

* Thu Mar 27 2008 Phil Knirsch <pknirsch@redhat.com> - 1.25-3
- Specfile cleanup, removal of static development libraries (#226414)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.25-2
- Autorebuild for GCC 4.3

* Mon Oct 22 2007 Phil Knirsch <pknirsch@redhat.com> - 1.25-1
- Fixed URLs
- Updated to sg3_utils-1.25

* Thu Aug 16 2007 Phil Knirsch <pknirsch@redhat.com> - 1.23-2
- License review and update

* Fri Feb 02 2007 Phil Knirsch <pknirsch@redhat.com> - 1.23-1
- Update to sg3_utils-1.23
- Updated summary

* Mon Nov 13 2006 Phil Knirsch <pknirsch@redhat.com> - 1.22-1
- Update to sg3_utils-1.22

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.20-2.1
- rebuild

* Wed Jun 07 2006 Phil Knirsch <pknirsch@redhat.com> - 1.20-2
- Fixed rebuild problem on latest toolchain
- Added missing buildprereqs

* Fri May 19 2006 Phil Knirsch <pknirsch@redhat.com> - 1.20-1
- Update to sg3_utils-1.20.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.19-1.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Phil Knirsch <pknirsch@redhat.com> - 1.19-1
- Update to sg3_utils-1.19.
- Fixed rebuild problem on 64bit archs.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.17-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Nov 07 2005 Phil Knirsch <pknirsch@redhat.com> 1.17-1
- Update to sg3-utils-1.17
- Split package up into 3 subpackages: sg3_utils, devel and libs
- Some minor updates to the specfile

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 1.06-5
- bump release and rebuild with gcc 4

* Fri Feb 18 2005 Phil Knirsch <pknirsch@redhat.com> 1.06-4
- rebuilt

* Tue Aug 03 2004 Phil Knirsch <pknirsch@redhat.com> 1.06-3
- rebuilt

* Thu Mar 11 2004 Tim Powers <timp@redhat.com> 1.06-2
- rebuild

* Wed Feb 18 2004 Phil Knirsch <pknirsch@redhat.com> 1.06-1
- Initial version for RHEL3 U2.

* Fri Jan 09 2004 - dgilbert@interlog.com
- sg3_utils.spec for mandrake; more sginfo work, sg_scan, sg_logs
  * sg3_utils-1.06

* Wed Nov 12 2003 - dgilbert@interlog.com
- sg_readcap: sizes; sg_logs: double fetch; sg_map 256 sg devices; sginfo
  * sg3_utils-1.05

* Tue May 13 2003 - dgilbert@interlog.com
- default sg_turs '-n=' to 1, sg_logs gets '-t' for temperature, CREDITS
  * sg3_utils-1.04

* Wed Apr 02 2003 - dgilbert@interlog.com
- 6 byte CDBs for sg_modes, sg_start on block devs, sg_senddiag, man pages
  * sg3_utils-1.03

* Wed Jan 01 2003 - dgilbert@interlog.com
- interwork with block SG_IO, fix in sginfo, '-t' for sg_turs
  * sg3_utils-1.02

* Wed Aug 14 2002 - dgilbert@interlog.com
- raw switch in sg_inq
  * sg3_utils-1.01

* Sun Jul 28 2002 - dgilbert@interlog.com
- decode sg_logs pages, add dio to sgm_dd, drop "gen=1" arg, "of=/dev/null"
  * sg3_utils-1.00

* Sun Mar 17 2002 - dgilbert@interlog.com
- add sg_modes+sg_logs for sense pages, expand sg_inq, add fua+sync to sg_dd++
  * sg3_utils-0.99

* Sat Feb 16 2002 - dgilbert@interlog.com
- resurrect sg_reset; snprintf cleanup, time,gen+cdbsz args to sg_dd++
  * sg3_utils-0.98

* Sun Dec 23 2001 - dgilbert@interlog.com
- move isosize to archive directory; now found in util-linux-2.10s and later
  * sg3_utils-0.97

* Fri Dec 21 2001 - dgilbert@interlog.com
- add sgm_dd, sg_read, sg_simple4 and sg_simple16 [add mmap-ed IO support]
  * sg3_utils-0.96

* Sun Sep 15 2001 - dgilbert@interlog.com
- sg_map can do inquiry; sg_dd, sgp_dd + sgq_dd dio help
  * sg3_utils-0.95

* Sun Apr 19 2001 - dgilbert@interlog.com
- add sg_start, improve sginfo and sg_map [Kurt Garloff]
  * sg3_utils-0.94

* Sun Mar 5 2001 - dgilbert@interlog.com
- add scsi_devfs_scan, add sg_include.h, 'coe' more general in sgp_dd
  * sg3_utils-0.93

* Tue Jan 16 2001 - dgilbert@interlog.com
- clean sg_err.h include dependencies, bug fixes, Makefile in archive directory
  * sg3_utils-0.92

* Mon Dec 21 2000 - dgilbert@interlog.com
- signals for sg_dd, man pages and additions for sg_rbuf and isosize
  * sg3_utils-0.91

* Mon Dec 11 2000 - dgilbert@interlog.com
- Initial creation of package, containing
  * sg3_utils-0.90
