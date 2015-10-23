%define name lsvpd
%define version 1.7.5

# Change the release number here
%define relver	1

Name:		%{name}
Version:	%{version}
Release:	%{relver}%{?dist}
Summary:	VPD/hardware inventory utilities for Linux

Group:		Applications/System
License:	GPLv2+
Vendor:		IBM Corp.
URL:		http://linux-diag.sf.net/Lsvpd.html
Source:		http://downloads.sourceforge.net/linux-diag/files/%{name}-new/%{version}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0:		Build.patch

Requires:	/bin/sed
Requires:	iprutils >= 2.3.12
Requires(pre):	iprutils >= 2.3.12
Requires(postun): iprutils >= 2.3.12

BuildRequires:	gcc-c++
BuildRequires:	librtas-devel
%if 0%{?suse_version}
BuildRequires:	libvpd2-devel
%endif
%if 0%{?rhel_version}
BuildRequires:	libvpd-devel
%endif
BuildRequires:	librtas-devel
BuildRequires:	zlib-devel
BuildRequires:	sg3_utils-devel
BuildRequires:	automake
BuildRequires:	libtool

%description
The lsvpd package contains all of the lsvpd, lscfg and lsmcode commands.
These commands, along with a scanning program called vpdupdate, constitute
a hardware inventory system. The lsvpd command provides Vital Product Data
(VPD) about hardware components to higher-level serviceability tools. The
lscfg command provides a more human-readable format of the VPD, as well as
some system-specific information. lsmcode lists microcode and firmware
levels. lsvio lists virtual devices, usually only found on POWER PC based
systems.

%prep
%setup -q
%patch0 -p1

%build
%if 0%{?suse_version}
export CFLAGS="%{optflags} -UPCI_IDS -DPCI_IDS='\"/usr/share/pci.ids\"' -UUSB_IDS -DUSB_IDS='\"/usr/share/usb.ids\"'"
export CXXFLAGS="%{optflags} -UPCI_IDS -DPCI_IDS='\"/usr/share/pci.ids\"' -UUSB_IDS -DUSB_IDS='\"/usr/share/usb.ids\"'"
%endif
./bootstrap.sh
%configure
%{__make} %{?_smp_mflags}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
%if 0%{?suse_version}
mkdir %{buildroot}/sbin
for i in lscfg lsmcode lsvio lsvpd update-lsvpd-db
do
 if test -f %{buildroot}%{_sbindir}/$i
 then
   ln -sfvbn ../usr/sbin/$i %{buildroot}/sbin/$i
 fi
done

if [ -e /etc/udev/rules.d/99-lsvpd.rules ]; then
	rm /etc/udev/rules.d/99-lsvpd.rules
fi
if [ -e /etc/udev/rules.d/99-lsvpd.disabled ]; then
	rm /etc/udev/rules.d/99-lsvpd.disabled 
fi
%endif

%post
if [ -d /var/lib/lsvpd ]; then
 rm -rf /var/lib/lsvpd
fi
%{_sbindir}/vpdupdate || :
# Ignore the vpdupdate failures and enforce a success
exit 0

%files
%defattr(-,root,root,-)
%doc COPYING README
%dir %{_sysconfdir}/lsvpd
%attr (644,root,root) %config %{_sysconfdir}/lsvpd/*
%if 0%{?rhel_version}
%{_sbindir}/*
%endif
%if 0%{?suse_version}
/sbin/*
%endif
%attr (755,root,root) %{_sbindir}/*
%{_mandir}/*/*

%if 0%{?rhel_version}
%config %{_sysconfdir}/lsvpd/scsi_templates.conf
%config %{_sysconfdir}/lsvpd/cpu_mod_conv.conf
%endif

%changelog
* Wed Aug 13 2014 - Vasant Hegde <hegdevasant@linux.vnet.ibm.com> - 1.7.5
- Added LE support
- Fixed couple of issues in build tools
- Removed outdated debian build code

* Mon Mar 17 2014 - Vasant Hegde <hegdevasant@linux.vnet.ibm.com> - 1.7.4
- Added support to parse VPD on PowerNV platform
- Filter out known paths from device-tree scan
- Minor fix in lsmcode output
- Added platform check to VPD tools
- Filter directories from device scan
- Fix possible out of range issue in substr operation
- Display FirmwareVersion and FirmwareLevel

* Thu Nov 14 2013 -  Suzuki Poulose <suzuki@in.ibm.com> - 1.7.3
- IBMinvscout: Removed from lsvpd package. Moving to a new package.
- vpdupdate: Filter ibm,bsr entries from VPD db.

* Thu Aug 22 2013 - Vasant Hegde <hegdevasant@linux.vnet.ibm.com> - 1.7.2
- vpdupdate: Find the PCI/USB ids files at runtime
- lscfg: allow -z, -d with -p
- lsvpd.spec.in: run vpdupdate in background post rpm install

* Wed Feb 20 2013 - Vasant Hegde <hegdevasant@linux.vnet.ibm.com> - 1.7.1-3
- Remove unused variables in invscout, lscfg.
- lscfg -vp: Skip empty record
- lscfg: Display Microcode Image level (MI)

* Fri Feb 15 2013 - Vasant Hegde <hegdevasant@linux.vnet.ibm.com> - 1.7.1-2
- "lscfg -vpl sysplaner0" ouptut alignment fix
- Display "Machine Model" information in lscfg output

* Fri Jan 28 2013 - Harsh P Bora <harsh@linux.vnet.ibm.com> - 1.7.1
- Support for device listing using location code with lsvpd -l
- Added man page for invscout
- Man pages updated to remove license info.
- Man pages updated to use correct vpd DB filename, document -l feature.

* Mon Sep 10 2012 - Suzuki Poulose <suzuki@in.ibm.com> - 1.7.0
- Added invscout tool.
- Better support for SCSI Enclosures

* Fri Mar 21 2008 - Eric Munson <ebmunson@us.ibm.com> - 1.6.3-1
- Adding proper conf file handling
- Removing executable bit on config and documentation files
- Removing second listing for config files

* Fri Mar 14 2008 - Eric Munson <ebmunson@us.ibm.com> - 1.6.2-3
- Becuase librtas is not yet in Fedora, the extra ppc dependency should
  be ignored

* Thu Mar 13 2008 - Eric Munson <ebmunson@us.ibm.com> - 1.6.2-2
- Adding arch check for ppc[64] dependency.

* Tue Mar 4 2008 - Eric Munson <ebmunson@us.ibm.com> - 1.6.2-1
- Updating for lsvpd-1.6.2

* Tue Mar 3 2008 - Eric Munson <ebmunson@us.ibm.com> - 1.6.1-1
- Updating for lsvpd-1.6.1

* Sat Feb 2 2008 - Eric Munson <ebmunson@us.ibm.com> - 1.6.0-1
- Updating lsvpd to use the new libvpd-2.0.0
- Removing %%{_mandir}/man8/* from %%files and replacing it with each
  individual file installed in the man8 directory

* Fri Dec 7 2007 - Brad Peters <bpeters@us.ibm.com> - 1.5.0
- Major changes in device detection code, basing detection on /sys/devices
  rather than /sys/bus as before
- Enhanced aggressiveness of AIX naming, ensuring that every detected device
  has at least one AIX name, and thus appears in lscfg output
- Changed method for discovering /sys/class entries
- Added some new VPD fields, one example of which is the device driver
  associated with the device
- Some minor changes to output formating
- Some changes to vpd collection
- Removing unnecessary Requires field

* Fri Nov 16 2007 - Eric Munson <ebmunson@us.ibm.com> - 1.4.0-1
- Removing udev rules from install as they are causing problems.  Hotplug 
  will be disabled until we find a smarter way of handling it.
- Updating License
- Adjusting the way vpdupdater is inserted into run control
- Removing #! from the beginning of the file.
- Fixes requested by Fedora Community

* Wed Oct 30 2007 - Eric Munson <ebmunson@us.ibm.com> - 1.3.5-1
- Remove calls to ldconfig
