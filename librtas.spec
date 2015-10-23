#
# spec file for package librtas
#
# Copyright (c) 2015 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           librtas
BuildRequires:  doxygen
Version:        1.3.13
Release:        0
BuildRequires:  fdupes
Summary:        Libraries to provide access to RTAS calls and RTAS events
License:        CPL-1.0
Group:          System/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
ExclusiveArch:  ppc ppc64 ppc64le
Url:            http://librtas.ozlabs.org/
Source0:        http://sourceforge.net/projects/librtas/files/librtas-%{version}.tar.gz
Source1:        baselibs.conf
Patch:          librtas-failedmagic.patch

%description 
The librtas shared library provides userspace with an interface through
which certain RTAS calls can be made.  The library uses either of the
RTAS User Module or the RTAS system call to direct the kernel in making
these calls.

The librtasevent shared library provides users with a set of
definitions and common routines useful in parsing and dumping the
contents of RTAS events.

%package        devel
Summary:        Devel librtas files
Group:          Development/Libraries/C and C++
Requires:       librtas1 = %{version}

%description devel
This package provides devel files of librtas

%package        doc
Summary:        Documentation for librtas
Group:          Documentation/Other

%description doc
This package provides librtas documentation

%package     -n librtas1
Summary:        Libraries to provide access to RTAS calls and RTAS events
Group:          System/Libraries

%description -n librtas1
The librtas shared library provides userspace with an interface through
which certain RTAS calls can be made.  The library uses either of the
RTAS User Module or the RTAS system call to direct the kernel in making
these calls.

The librtasevent shared library provides users with a set of
definitions and common routines useful in parsing and dumping the
contents of RTAS events.

%prep
%setup -q
%patch

sed s,rtasevent,ofdt,g <doxygen.rtasevent >doxygen.ofdt

%build
make CFLAGS="%optflags -fPIC -g -I $PWD/librtasevent_src" LIB_DIR="%{_libdir}" %{?_smp_mflags}

%install
rm -rf doc/*/latex
make install DESTDIR=%buildroot LIB_DIR="%{_libdir}"
%fdupes %buildroot/%_docdir
/sbin/ldconfig -n %buildroot%{_libdir}

%post -n librtas1 -p /sbin/ldconfig

%postun -n librtas1 -p /sbin/ldconfig

%files -n librtas1
%doc Changelog
%defattr(-, root, root)
%{_libdir}/lib*.so.*

%files devel
%defattr(-, root, root)
/usr/include/*
%{_libdir}/librtasevent.so
%{_libdir}/librtas.so
%{_libdir}/libofdt.so

%files doc
%defattr(-, root, root)
%doc %{_docdir}/librtas 

%changelog

