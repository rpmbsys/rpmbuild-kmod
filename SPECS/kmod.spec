Name:		kmod
Version:	28
Release:	2%{?dist}
Summary:	Linux kernel module management utilities

License:	GPLv2+
URL:		http://git.kernel.org/?p=utils/kernel/kmod/kmod.git;a=summary
Source0:	https://www.kernel.org/pub/linux/utils/kernel/kmod/%{name}-%{version}.tar.xz
Source1:	weak-modules
Exclusiveos:	Linux

BuildRequires:  gcc
BuildRequires:	chrpath
BuildRequires:	zlib-devel
BuildRequires:	xz-devel
BuildRequires:  libxslt
%if 0%{?rhel} == 7
BuildRequires:  openssl11-devel
BuildRequires:  pkgconfig
%else
BuildRequires:  openssl-devel
%endif
BuildRequires:  make
BuildRequires:  libzstd-devel

Provides:	module-init-tools = 4.0-1
Obsoletes:	module-init-tools < 4.0-1
Provides:	/sbin/modprobe

%if 0%{?rhel} == 7
Requires:  openssl11-libs
%endif

%description
The kmod package provides various programs needed for automatic
loading and unloading of modules under 2.6, 3.x, and later kernels, as well
as other module management programs. Device drivers and filesystems are two
examples of loaded and unloaded modules.

%package libs
Summary:	Libraries to handle kernel module loading and unloading
License:	LGPLv2+

%description libs
The kmod-libs package provides runtime libraries for any application that
wishes to load or unload Linux kernel modules from the running system.

%package devel
Summary:	Header files for kmod development
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The kmod-devel package provides header files used for development of
applications that wish to load or unload Linux kernel modules.

%prep
%autosetup -p1

%build
%configure \
  --with-zlib \
  --with-xz \
  --with-zstd \
%if 0%{?rhel} == 7
  --with-openssl libcrypto_CFLAGS="$(pkg-config --cflags libcrypto11)" libcrypto_LIBS="$(pkg-config --libs libcrypto11)" CFLAGS="$(pkg-config --cflags openssl11)" LDFLAGS="$(pkg-config --libs openssl11)"
%else
  --with-openssl
%endif

%{make_build} V=1

%install
%{make_install}

pushd $RPM_BUILD_ROOT/%{_mandir}/man5
ln -s modprobe.d.5.gz modprobe.conf.5.gz
popd

find %{buildroot} -type f -name "*.la" -delete

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/modprobe
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/modinfo
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/insmod
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/rmmod
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/depmod
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/lsmod

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/modprobe.d

mkdir -p $RPM_BUILD_ROOT/sbin
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/weak-modules

%files
%dir %{_sysconfdir}/depmod.d
%dir %{_sysconfdir}/modprobe.d
%dir %{_prefix}/lib/modprobe.d
%{_bindir}/kmod
%{_sbindir}/modprobe
%{_sbindir}/modinfo
%{_sbindir}/insmod
%{_sbindir}/rmmod
%{_sbindir}/lsmod
%{_sbindir}/depmod
%{_sbindir}/weak-modules
%{_datadir}/bash-completion/
%attr(0644,root,root) %{_mandir}/man5/*.5*
%attr(0644,root,root) %{_mandir}/man8/*.8*
%doc NEWS README TODO

%files libs
%license COPYING
%{_libdir}/libkmod.so.*

%files devel
%{_includedir}/libkmod.h
%{_libdir}/pkgconfig/libkmod.pc
%{_libdir}/libkmod.so

%changelog
* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 07 2021 Josh Boyer <jwboyer@fedoraproject.org> - 28-1
- New upstream v28
- Enable zstd support
- Resolves: rhbz#1913949

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Mar 25 2020 Yauheni Kaliuta <ykaliuta@fedoraproject.org> - 27-2
- add 0001-depmod-do-not-output-.bin-to-stdout.patch
  Resolves: rhbz#1808430

* Thu Feb 20 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 27-1
- New upstream v27

* Mon Jan 20 2020 Yauheni Kaliuta <ykaliuta@fedoraproject.org> - 26-5
- weak-modules: sync with RHEL

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 25 2019 Yauheni Kaliuta <yauheni.kaliuta@redhat.com> - 26-3
- weak-modules: sync with RHEL

* Sun Feb 24 2019 Yauheni Kaliuta <ykaliuta@fedoraproject.org> - 26-2
- add PKCS7/openssl support (rhbz 1320921)

* Sun Feb 24 2019 Yauheni Kaliuta <ykaliuta@fedoraproject.org> - 26-1
- Update to version 26 (rhbz 1673749)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 29 2018 James Antill <james.antill@redhat.com> - 25-4
- Remove ldconfig scriptlet, now done via. transfiletrigger in glibc (rhbz 1644063)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Josh Boyer <jwboyer@fedoraproject.org> - 25-1
- Update to version 25 (rhbz 1532597)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 24 2017 Josh Boyer <jwboyer@fedoraproject.org> - 24-1
- Update to version 24 (rhbz 1426589)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul 22 2016 Josh Boyer <jwboyer@fedoraproject.org> - 23-1
- Update to version 23

* Thu Feb 25 2016 Peter Robinson <pbrobinson@fedoraproject.org> 22-4
- Add powerpc patch to fix ToC on 4.5 ppc64le kernel

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 07 2016 Josh Boyer <jwboyer@fedoraproject.org> - 22-2
- Fix path to dracut in weak-modules (rhbz 1295038)

* Wed Nov 18 2015 Josh Boyer <jwboyer@fedoraproject.org> - 22-1
- Update to version 22

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Ville Skyttä <ville.skytta@iki.fi> - 21-2
- Own bash completion dirs not owned by anything in dep chain

* Tue Jun 09 2015 Josh Boyer <jwboyer@fedoraproject.org> - 21-1
- Update to verion 21

* Mon Mar 02 2015 Josh Boyer <jwboyer@fedoraproject.org> - 20.1
- Update to version 20

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 19-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Nov 16 2014 Josh Boyer <jwboyer@fedoraproject.org> - 19-1
- Update to version 19

* Wed Oct 29 2014 Josh Boyer <jwboyer@fedoraproject.org> - 18-4
- Backport patch to fix device node permissions (rhbz 1147248)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 18-2
- fix license handling

* Tue Jun 24 2014 Josh Boyer <jwboyer@fedoraproject.org> - 18-1
- Update to version 18

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 09 2014 Josh Boyer <jwboyer@fedoraproject.org> - 17-1
- Update to version 17

* Thu Jan 02 2014 Václav Pavlín <vpavlin@redhat.com> - 16-1
- Update to version 16

* Thu Aug 22 2013 Josh Boyer <jwboyer@fedoraproject.org> - 15-1
- Update to version 15

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 05 2013 Josh Boyer <jwboyer@redhat.com> - 14-1
- Update to version 14

* Fri Apr 19 2013 Václav Pavlín <vpavlin@redhat.com> - 13-2
- Main package should require -libs

* Wed Apr 10 2013 Josh Boyer <jwboyer@redhat.com> - 13-1
- Update to version 13

* Wed Mar 20 2013 Weiping Pan <wpan@redhat.com> - 12-3
- Pull in weak-modules for kABI from Jon Masters <jcm@redhat.com> 

* Mon Mar 18 2013 Josh Boyer <jwboyer@redhat.com>
- Add patch to make rmmod understand built-in modules (rhbz 922187)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Josh Boyer <jwboyer@redhat.com>
- Update to version 12

* Thu Nov 08 2012 Josh Boyer <jwboyer@redhat.com>
- Update to version 11

* Fri Sep 07 2012 Josh Boyer <jwboyer@redaht.com>
- Update to version 10

* Mon Aug 27 2012 Josh Boyer <jwboyer@redhat.com>
- Update to version 9

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Josh Boyer <jwboyer@redhat.com> - 8-2
- Provide modprobe.conf(5) (rhbz 824552)

* Tue May 08 2012 Josh Boyer <jwboyer@redhat.com> - 8-1
- Update to version 8

* Mon Mar 19 2012 Kay Sievers <kay@redhat.com> - 7-1
- update to version 7
  - fix issue with --show-depends, where built-in
    modules of the running kernel fail to include
    loadable modules of the kernel specified

* Sun Mar 04 2012 Kay Sievers <kay@redhat.com> - 6-1
- update to version 6
- remove all patches, they are included in the release

* Fri Feb 24 2012 Kay Sievers <kay@redhat.com> - 5-8
- try to address brc#771285

* Sun Feb 12 2012 Kay Sievers <kay@redhat.com> - 5-7
- fix infinite loop with softdeps

* Thu Feb 09 2012 Harald Hoyer <harald@redhat.com> 5-6
- add upstream patch to fix "modprobe --ignore-install --show-depends"
  otherwise dracut misses a lot of modules, which are already loaded

* Wed Feb 08 2012 Harald Hoyer <harald@redhat.com> 5-5
- add "lsmod"

* Tue Feb  7 2012 Kay Sievers <kay@redhat.com> - 5-4
- remove temporarily added fake-provides

* Tue Feb  7 2012 Kay Sievers <kay@redhat.com> - 5-3
- temporarily add fake-provides to be able to bootstrap
  the new udev which pulls the old udev into the buildroot

* Tue Feb  7 2012 Kay Sievers <kay@redhat.com> - 5-1
- Update to version 5
- replace the module-init-tools package and provide all tools
  as compatibility symlinks

* Mon Jan 16 2012 Kay Sievers <kay@redhat.com> - 4-1
- Update to version 4
- set --with-rootprefix=
- enable zlib and xz support

* Thu Jan 05 2012 Jon Masters <jcm@jonmasters.org> - 3-1
- Update to latest upstream (adds new depmod replacement utility)
- For the moment, use the "kmod" utility to test the various functions

* Fri Dec 23 2011 Jon Masters <jcm@jonmasters.org> - 2-6
- Update kmod-2-with-rootlibdir patch with rebuild automake files

* Fri Dec 23 2011 Jon Masters <jcm@jonmasters.org> - 2-5
- Initial build for Fedora following package import

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-4
- There is no generic macro for non-multilib "/lib", hardcode like others

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-3
- Update package incorporating fixes from initial review feedback
- Cleaups to SPEC, rpath, documentation, library and binary locations

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-2
- Update package for posting to wider test audience (initial review submitted)

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-1
- Initial Fedora package for module-init-tools replacement (kmod) library
