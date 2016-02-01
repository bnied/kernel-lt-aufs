%global __spec_install_pre %{___build_pre}

# Define the version of the Linux Kernel Archive tarball.
%define LKAver 4.3.5

# Define the version of the aufs-standalone tarball
%define AUFSver aufs-standalone

# Define the buildid, if required.
#define buildid .

# The following build options are enabled by default.
# Use either --without <option> on your rpmbuild command line
# or force the values to 0, here, to disable them.

# kernel-ml-aufs
%define with_default %{?_without_default: 0} %{?!_without_default: 1}
# kernel-ml-aufs-doc
%define with_doc     %{?_without_doc:     0} %{?!_without_doc:     1}
# kernel-ml-aufs-headers
%define with_headers %{?_without_headers: 0} %{?!_without_headers: 1}
# perf
%define with_perf    %{?_without_perf:    0} %{?!_without_perf:    1}
# tools
%define with_tools   %{?_without_tools:   0} %{?!_without_tools:   1}

# These architectures install vdso/ directories.
%define vdso_arches i686 x86_64

# Architecture defaults.
%define asmarch x86
%define buildarch %{_target_cpu}
%define hdrarch %{_target_cpu}

# Per-architecture tweaks.

%ifarch noarch
# Documentation only.
%define with_default 0
%define with_headers 0
%define with_perf 0
%define with_tools 0
%endif

%ifarch i686
# 32-bit kernel-ml-aufs, headers, perf & tools.
%define buildarch i386
%define hdrarch i386
%define with_doc 0
%endif

%ifarch x86_64
# 64-bit kernel-ml-aufs, headers, perf & tools.
%define with_doc 0
%endif

# Determine the sublevel number and set pkg_version.
%define sublevel %(echo %{LKAver} | %{__awk} -F\. '{ print $3 }')
%if "%{sublevel}" == ""
%define pkg_version %{LKAver}.0
%else
%define pkg_version %{LKAver}
%endif

# Set pkg_release.
%define pkg_release 1%{?buildid}%{?dist}

#
# Three sets of minimum package version requirements in the form of Conflicts.
#

#
# First the general kernel required versions, as per Documentation/Changes.
#
%define kernel_dot_org_conflicts ppp < 2.4.3-3, isdn4k-utils < 3.2-32, nfs-utils < 1.0.7-12, e2fsprogs < 1.37-4, util-linux < 2.12, jfsutils < 1.1.7-2, reiserfs-utils < 3.6.19-2, xfsprogs < 2.6.13-4, procps < 3.2.5-6.3, oprofile < 0.9.1-2, device-mapper-libs < 1.02.63-2, mdadm < 3.2.1-5

#
# Then a series of requirements that are distribution specific, either
# because we add patches for something or the older versions have
# problems with the newer kernel or lack certain things that make
# integration in the distro harder than needed.
#
%define package_conflicts initscripts < 7.23, udev < 063-6, iptables < 1.3.2-1, ipw2200-firmware < 2.4, iwl4965-firmware < 228.57.2, selinux-policy-targeted < 1.25.3-14, squashfs-tools < 4.0, wireless-tools < 29-3

# We moved the drm include files into kernel-headers, make sure there's
# a recent enough libdrm-devel on the system that doesn't have those.
%define kernel_headers_conflicts libdrm-devel < 2.4.0-0.15

#
# Packages that need to be installed before the kernel because the %%post scripts make use of them.
#
%define kernel_prereq fileutils, module-init-tools >= 3.16-2, initscripts >= 8.11.1-1, grubby >= 8.28-2
%define initrd_prereq dracut >= 001-7

Name: kernel-ml-aufs
Summary: The Linux kernel. (The core of any Linux-based operating system.)
Group: System Environment/Kernel
License: GPLv2
URL: https://www.kernel.org/
Version: %{pkg_version}
Release: %{pkg_release}
##################################
#ExclusiveArch: noarch i686 x86_64
ExclusiveArch: noarch x86_64
##################################
ExclusiveOS: Linux
Provides: kernel = %{version}-%{release}
Provides: kernel-%{_target_cpu} = %{version}-%{release}
Provides: kernel-uname-r = %{version}-%{release}.%{_target_cpu}
Provides: kernel-drm = 4.3.0
Provides: kernel-drm-nouveau = 16
Provides: kernel-modeset = 1
Provides: %{name} = %{version}-%{release}
Provides: %{name}-%{_target_cpu} = %{version}-%{release}
Provides: %{name}-uname-r = %{version}-%{release}.%{_target_cpu}
Provides: %{name}-drm = 4.3.0
Provides: %{name}-drm-nouveau = 16
Provides: %{name}-modeset = 1
Requires(pre): %{kernel_prereq}
Requires(pre): %{initrd_prereq}
Requires(pre): linux-firmware >= 20100806-2
Requires(post): %{_sbindir}/new-kernel-pkg
Requires(preun): %{_sbindir}/new-kernel-pkg
Conflicts: %{kernel_dot_org_conflicts}
Conflicts: %{package_conflicts}
# We can't let RPM do the dependencies automatic because it'll then pick up
# a correct but undesirable perl dependency from the module headers which
# isn't required for the kernel proper to function
AutoReq: no
AutoProv: yes

#
# List the packages used during the kernel build
#
BuildRequires: asciidoc, bash >= 2.03, bc, binutils >= 2.12, diffutils, findutils
BuildRequires: gawk, gcc >= 3.4.2, gzip, hostname, m4, make >= 3.78, module-init-tools
BuildRequires: net-tools, openssl, openssl-devel, patch >= 2.5.4, perl
BuildRequires: redhat-rpm-config >= 9.1.0-55, sh-utils, tar, xmlto, xz
%if %{with_perf}
BuildRequires: audit-libs-devel, binutils-devel, bison, elfutils-devel, newt-devel, numactl-devel,
BuildRequires: perl(ExtUtils::Embed), python-devel, slang-devel, xz-devel, zlib-devel
%endif
%if %{with_tools}
BuildRequires: gettext, pciutils, pciutils-devel, zlib-devel
%endif

# Sources.
Source0: ftp://ftp.kernel.org/pub/linux/kernel/v4.x/linux-%{LKAver}.tar.xz
#######################################
#Source1: config-%{version}-i686
#Source2: config-%{version}-i686-NONPAE
#######################################
Source3: config-%{version}-x86_64
Source4: cpupower.service
Source5: cpupower.config
Source6: %{AUFSver}.tar

%description
This package provides the Linux kernel (vmlinuz), the core of any
Linux-based operating system. The kernel handles the basic functions
of the OS: memory allocation, process allocation, device I/O, etc.

%package devel
Summary: Development package for building modules to match the kernel.
Group: System Environment/Kernel
Provides: kernel-devel = %{version}-%{release}
Provides: kernel-devel-%{_target_cpu} = %{version}-%{release}
Provides: kernel-devel-uname-r = %{version}-%{release}.%{_target_cpu}
Provides: %{name}-devel = %{version}-%{release}
Provides: %{name}-devel-%{_target_cpu} = %{version}-%{release}
Provides: %{name}-devel-uname-r = %{version}-%{release}.%{_target_cpu}
AutoReqProv: no
Requires(pre): /usr/bin/find
Requires: perl
%description devel
This package provides the kernel header files and makefiles
sufficient to build modules against the kernel package.

%if %{with_doc}
%package doc
Summary: Various bits of documentation found in the kernel sources.
Group: Documentation
Provides: kernel-doc = %{version}-%{release}
Provides: %{name}-doc = %{version}-%{release}
Conflicts: kernel-doc < %{version}-%{release}
%description doc
This package provides documentation files from the kernel sources.
Various bits of information about the Linux kernel and the device
drivers shipped with it are documented in these files.

You'll want to install this package if you need a reference to the
options that can be passed to the kernel modules at load time.
%endif

%if %{with_headers}
%package headers
Summary: Header files of the kernel, for use by glibc.
Group: Development/System
Obsoletes: glibc-kernheaders < 3.0-46
Provides: glibc-kernheaders = 3.0-46
Provides: kernel-headers = %{version}-%{release}
Provides: %{name}-headers = %{version}-%{release}
Conflicts: kernel-headers < %{version}-%{release}
%description headers
This package provides the C header files that specify the interface
between the Linux kernel and userspace libraries & programs. The
header files define structures and constants that are needed when
building most standard programs. They are also required when
rebuilding the glibc package.
%endif

%if %{with_perf}
%package -n perf
Summary: Performance monitoring of the kernel.
Group: Development/System
License: GPLv2
%description -n perf
This package provides the perf tool and the supporting documentation
for performance monitoring of the Linux kernel.

%package -n python-perf
Summary: Python bindings for applications that will manipulate perf events.
Group: Development/Libraries
%description -n python-perf
This package provides a module that permits applications written in the
Python programming language to use the interface to manipulate perf events.

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

%if %{with_tools}
%package -n %{name}-tools
Summary: Assortment of tools for the kernel.
Group: Development/System
License: GPLv2
Provides:  cpupowerutils = 1:009-0.6.p1
Obsoletes: cpupowerutils < 1:009-0.6.p1
Provides:  cpufreq-utils = 1:009-0.6.p1
Obsoletes: cpufreq-utils < 1:009-0.6.p1
Provides:  cpufrequtils = 1:009-0.6.p1
Obsoletes: cpufrequtils < 1:009-0.6.p1
Obsoletes: cpuspeed < 1:2.0
Requires: %{name}-tools-libs = %{version}-%{release}
Conflicts: kernel-tools < %{version}-%{release}
%description -n %{name}-tools
This package contains the tools/ directory and its supporting
documentation, derived from the kernel source.

%package -n %{name}-tools-libs
Summary: Libraries for the kernel tools.
Group: Development/System
License: GPLv2
Conflicts: kernel-tools-libs < %{version}-%{release}
%description -n %{name}-tools-libs
This package contains the libraries built from the
tools/ directory, derived from the kernel source.

%package -n %{name}-tools-libs-devel
Summary: Development package for the kernel tools libraries.
Group: Development/System
License: GPLv2
Requires: %{name}-tools = %{version}-%{release}
Requires: %{name}-tools-libs = %{version}-%{release}
Provides:  cpupowerutils-devel = 1:009-0.6.p1
Obsoletes: cpupowerutils-devel < 1:009-0.6.p1
Provides: %{name}-tools-devel
Conflicts: kernel-tools-libs-devel < %{version}-%{release}
%description -n %{name}-tools-libs-devel
This package contains the development files for the tools/ directory
libraries, derived from the kernel source.
%endif

# Disable the building of the debug package(s).
%define debug_package %{nil}

%prep
%setup -q -n %{name}-%{version} -c
%{__mv} linux-%{LKAver} linux-%{version}-%{release}.%{_target_cpu}
mkdir %{AUFSver}
tar xf %{SOURCE6} -C %{AUFSver}
pushd linux-%{version}-%{release}.%{_target_cpu} > /dev/null
cp -r ../%{AUFSver}/Documentation/filesystems Documentation/
cp -r ../%{AUFSver}/Documentation/ABI Documentation/
cp -r ../%{AUFSver}/fs/aufs fs/
cp ../%{AUFSver}/include/uapi/linux/aufs_type.h include/uapi/linux/
patch -p 1 < ../%{AUFSver}/aufs4-kbuild.patch
patch -p 1 < ../%{AUFSver}/aufs4-base.patch
patch -p 1 < ../%{AUFSver}/aufs4-mmap.patch
%{__cp} %{SOURCE3} .
popd > /dev/null

%build
BuildKernel() {
    Flavour=$1

    %{__make} -s distclean

    # Select the correct flavour configuration file.
    if [ -z "${Flavour}" ]; then
        %{__cp} config-%{version}-%{_target_cpu} .config
    else
        %{__cp} config-%{version}-%{_target_cpu}-${Flavour} .config
    fi

    %define KVRFA %{version}-%{release}${Flavour}.%{_target_cpu}

    # Set the EXTRAVERSION string in the main Makefile.
    %{__perl} -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{release}${Flavour}.%{_target_cpu}/" Makefile

    %{__make} -s ARCH=%{buildarch} %{?_smp_mflags} bzImage
    %{__make} -s ARCH=%{buildarch} %{?_smp_mflags} modules

    # Install the results into the RPM_BUILD_ROOT directory.
    %{__mkdir_p} $RPM_BUILD_ROOT/boot
    %{__install} -m 644 .config $RPM_BUILD_ROOT/boot/config-%{KVRFA}
    %{__install} -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-%{KVRFA}

    # We estimate the size of the initramfs because rpm needs to take this size
    # into consideration when performing disk space calculations. (See bz #530778)
    dd if=/dev/zero of=$RPM_BUILD_ROOT/boot/initramfs-%{KVRFA}.img bs=1M count=20

    %{__cp} arch/x86/boot/bzImage $RPM_BUILD_ROOT/boot/vmlinuz-%{KVRFA}
    %{__chmod} 755 $RPM_BUILD_ROOT/boot/vmlinuz-%{KVRFA}

    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/kernel
    # Override $(mod-fw) because we don't want it to install any firmware.
    # We'll get it from the linux-firmware package and we don't want conflicts.
    %{__make} -s ARCH=%{buildarch} INSTALL_MOD_PATH=$RPM_BUILD_ROOT KERNELRELEASE=%{KVRFA} modules_install mod-fw=

%ifarch %{vdso_arches}
    %{__make} -s ARCH=%{buildarch} INSTALL_MOD_PATH=$RPM_BUILD_ROOT KERNELRELEASE=%{KVRFA} vdso_install
    /usr/bin/find $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/vdso -type f -name 'vdso*.so' | xargs --no-run-if-empty %{__strip}
    if grep '^CONFIG_XEN=y$' .config > /dev/null; then
        echo > ldconfig-%{name}.conf "\
# This directive teaches ldconfig to search in nosegneg subdirectories
# and cache the DSOs there with extra bit 1 set in their hwcap match
# fields.  In Xen guest kernels, the vDSO tells the dynamic linker to
# search in nosegneg subdirectories and to match this extra hwcap bit
# in the ld.so.cache file.
hwcap 1 nosegneg"
    fi
    if [ ! -s ldconfig-%{name}.conf ]; then
        echo > ldconfig-%{name}.conf "\
# Placeholder file, no vDSO hwcap entries used in this kernel."
    fi
    %{__install} -D -m 444 ldconfig-%{name}.conf $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{KVRFA}.conf
%endif

    # Save the headers/makefiles, etc, for building modules against.
    #
    # This looks scary but the end result is supposed to be:
    #
    # - all arch relevant include/ files
    # - all Makefile & Kconfig files
    # - all script/ files
    #
    %{__rm} -f $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    %{__rm} -f $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/source
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    pushd $RPM_BUILD_ROOT/lib/modules/%{KVRFA} > /dev/null
    %{__ln_s} build source
    popd > /dev/null
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/extra
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/updates
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/weak-updates

    # First copy everything . . .
    %{__cp} --parents `/usr/bin/find  -type f -name 'Makefile*' -o -name 'Kconfig*'` $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    %{__cp} Module.symvers $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    %{__cp} System.map $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    if [ -s Module.markers ]; then
        %{__cp} Module.markers $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    fi

    %{__gzip} -c9 < Module.symvers > $RPM_BUILD_ROOT/boot/symvers-%{KVRFA}.gz

    # . . . then drop all but the needed Makefiles & Kconfig files.
    %{__rm} -rf $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/Documentation
    %{__rm} -rf $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/scripts
    %{__rm} -rf $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include
    %{__cp} .config $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    %{__cp} -a scripts $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    if [ -d arch/%{buildarch}/scripts ]; then
        %{__cp} -a arch/%{buildarch}/scripts $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/arch/%{_arch} || :
    fi
    if [ -f arch/%{buildarch}/*lds ]; then
        %{__cp} -a arch/%{buildarch}/*lds $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/arch/%{_arch}/ || :
    fi
    %{__rm} -f $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/scripts/*.o
    %{__rm} -f $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/scripts/*/*.o
    if [ -d arch/%{asmarch}/include ]; then
        %{__cp} -a --parents arch/%{asmarch}/include $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/
    fi
    if [ -d arch/%{asmarch}/syscalls ]; then
        %{__cp} -a --parents arch/%{asmarch}/syscalls $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/
    fi
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include
    pushd include > /dev/null
    %{__cp} -a * $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/
    popd > /dev/null
    %{__rm} -f $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/Kbuild
    # Ensure a copy of the version.h file is in the include/linux/ directory.
    %{__cp} usr/include/linux/version.h $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/linux/
    # Copy the generated autoconf.h file to the include/linux/ directory.
    %{__cp} include/generated/autoconf.h $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/linux/
    # Copy .config to include/config/auto.conf so a "make prepare" is unnecessary.
    %{__cp} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/.config $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/config/auto.conf
    # Now ensure that the Makefile, .config, auto.conf, autoconf.h and version.h files
    # all have matching timestamps so that external modules can be built.
    touch -r $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/Makefile $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/.config
    touch -r $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/Makefile $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/config/auto.conf
    touch -r $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/Makefile $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/linux/autoconf.h
    touch -r $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/Makefile $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/linux/version.h
    touch -r $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/Makefile $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/generated/autoconf.h
    touch -r $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/Makefile $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/generated/uapi/linux/version.h

    # Remove any 'left-over' .cmd files.
    /usr/bin/find $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build -type f -name '*.cmd' | xargs --no-run-if-empty %{__rm} -f

    /usr/bin/find $RPM_BUILD_ROOT/lib/modules/%{KVRFA} -type f -name '*.ko' > modnames

    # Mark the modules executable, so that strip-to-file can strip them.
    xargs --no-run-if-empty %{__chmod} u+x < modnames

    # Generate a list of modules for block and networking.
    grep -F /drivers/ modnames | xargs --no-run-if-empty nm -upA | sed -n 's,^.*/\([^/]*\.ko\):  *U \(.*\)$,\1 \2,p' > drivers.undef

    collect_modules_list()
    {
        sed -r -n -e "s/^([^ ]+) \\.?($2)\$/\\1/p" drivers.undef | LC_ALL=C sort -u > $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/modules.$1
        if [ ! -z "$3" ]; then
            sed -r -e "/^($3)\$/d" -i $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/modules.$1
        fi
    }

    collect_modules_list networking \
        'register_netdev|ieee80211_register_hw|usbnet_probe|phy_driver_register|rt2x00(pci|usb)_probe|register_netdevice'

    collect_modules_list block \
        'ata_scsi_ioctl|scsi_add_host|scsi_add_host_with_dma|blk_alloc_queue|blk_init_queue|register_mtd_blktrans|scsi_esp_register|scsi_register_device_handler|blk_queue_physical_block_size|pktcdvd.ko|dm-mod.ko'

    collect_modules_list drm \
        'drm_open|drm_init'

    collect_modules_list modesetting \
        'drm_crtc_init'

    # Detect any missing or incorrect license tags.
    %{__rm} -f modinfo

    while read i
    do
        echo -n "${i#$RPM_BUILD_ROOT/lib/modules/%{KVRFA}/} " >> modinfo
        %{_sbindir}/modinfo -l $i >> modinfo
    done < modnames

    grep -E -v 'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' modinfo && exit 1

    %{__rm} -f modinfo modnames

    # Remove all the files that will be auto generated by depmod at the kernel install time.
    for i in alias alias.bin builtin.bin ccwmap dep dep.bin ieee1394map inputmap isapnpmap ofmap pcimap seriomap symbols symbols.bin usbmap
    do
        %{__rm} -f $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/modules.$i
    done

    # Move the development files out of the /lib/modules/ file system.
    %{__mkdir_p} $RPM_BUILD_ROOT/usr/src/kernels
    %{__mv} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build $RPM_BUILD_ROOT/usr/src/kernels/%{KVRFA}
    %{__ln_s} -f /usr/src/kernels/%{KVRFA} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
}

# Prepare the directories.
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT/boot
%{__mkdir_p} $RPM_BUILD_ROOT%{_libexecdir}

pushd linux-%{version}-%{release}.%{_target_cpu} > /dev/null

%if %{with_default}
BuildKernel
%endif

%if %{with_doc}
# Make the HTML and man pages.
%{__make} -s htmldocs mandocs 2> /dev/null

# Sometimes non-world-readable files sneak into the kernel source tree.
%{__chmod} -R a=rX Documentation
/usr/bin/find Documentation -type d | xargs %{__chmod} u+w
%endif

%if %{with_perf}
%global perf_make \
    %{__make} -s -C tools/perf %{?_smp_mflags} WERROR=0 NO_LIBUNWIND=1 HAVE_CPLUS_DEMANGLE=1 NO_GTK2=1 NO_STRLCPY=1 prefix=%{_prefix}

%{perf_make} all
%{perf_make} man
%endif

%if %{with_tools}
%ifarch x86_64
# Make sure that version-gen.sh is executable.
%{__chmod} +x tools/power/cpupower/utils/version-gen.sh

%{__make} -s %{?_smp_mflags} -C tools/power/cpupower CPUFREQ_BENCH=false

pushd tools/power/cpupower/debug/x86_64 > /dev/null
%{__make} -s %{?_smp_mflags} centrino-decode powernow-k8-decode
popd > /dev/null

pushd tools/power/x86/x86_energy_perf_policy > /dev/null
%{__make} -s
popd > /dev/null

pushd tools/power/x86/turbostat > /dev/null
%{__make} -s
popd > /dev/null
%endif
%endif

popd > /dev/null

%install
pushd linux-%{version}-%{release}.%{_target_cpu} > /dev/null

%if %{with_headers}
# We have to do the headers install before the tools install because the
# kernel headers_install will remove any header files in /usr/include that
# it doesn't install itself.

# Install kernel headers
%{__make} -s ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install

# Do headers_check but don't die if it fails.
%{__make} -s ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_check > hdrwarnings.txt || :
if grep -q exist hdrwarnings.txt; then
    sed s:^$RPM_BUILD_ROOT/usr/include/:: hdrwarnings.txt
    # Temporarily cause a build failure if header inconsistencies.
    # exit 1
fi

# Remove the unrequired files.
/usr/bin/find $RPM_BUILD_ROOT/usr/include -type f \
    \( -name .install -o -name .check -o -name ..install.cmd -o -name ..check.cmd \) | \
    xargs --no-run-if-empty %{__rm} -f
%endif

%if %{with_doc}
DOCDIR=$RPM_BUILD_ROOT%{_datadir}/doc/%{name}-doc-%{version}
MAN9DIR=$RPM_BUILD_ROOT%{_datadir}/man/man9

# Copy the documentation over.
%{__mkdir_p} $DOCDIR
%{__tar} -f - --exclude=man --exclude='.*' -c Documentation | %{__tar} xf - -C $DOCDIR

# Install the man pages for the kernel API.
%{__mkdir_p} $MAN9DIR
/usr/bin/find Documentation/DocBook/man -type f -name '*.9.gz' -print0 \
    | xargs -0 --no-run-if-empty %{__cp} -u -t $MAN9DIR
/usr/bin/find $MAN9DIR -type f -name '*.9.gz' -print0 \
    | xargs -0 --no-run-if-empty %{__chmod} 444
ls $MAN9DIR | grep -q '' || > $MAN9DIR/BROKEN
%endif

%if %{with_perf}
# perf tool binary and supporting scripts/binaries.
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install

# perf-python extension.
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-python_ext

# perf man pages. (Note: implicit rpm magic compresses them later.)
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-man
%endif

%if %{with_tools}
%ifarch x86_64
%{__make} -s -C tools/power/cpupower DESTDIR=$RPM_BUILD_ROOT libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false install
%{__rm} -f %{buildroot}%{_libdir}/*.{a,la}
%find_lang cpupower
mv cpupower.lang ../
pushd tools/power/cpupower/debug/x86_64 > /dev/null
%{__install} -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
%{__install} -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
popd > /dev/null
%{__chmod} 0755 %{buildroot}%{_libdir}/libcpupower.so*
%{__mkdir_p} %{buildroot}%{_unitdir} %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m644 %{SOURCE4} %{buildroot}%{_unitdir}/cpupower.service
%{__install} -m644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/cpupower
%{__mkdir_p} %{buildroot}%{_mandir}/man8
pushd tools/power/x86/x86_energy_perf_policy > /dev/null
%{__make} -s DESTDIR=%{buildroot} install
popd > /dev/null
pushd tools/power/x86/turbostat > /dev/null
%{__make} -s DESTDIR=%{buildroot} install
popd > /dev/null
%endif
%endif

popd > /dev/null

%clean
%{__rm} -rf $RPM_BUILD_ROOT

# Scripts section.
%if %{with_default}
%posttrans
%{_sbindir}/new-kernel-pkg --package %{name} --mkinitrd --dracut --depmod --update %{version}-%{release}.%{_target_cpu} || exit $?
%{_sbindir}/new-kernel-pkg --package %{name} --rpmposttrans %{version}-%{release}.%{_target_cpu} || exit $?
if [ -x %{_sbindir}/weak-modules ]; then
    %{_sbindir}/weak-modules --add-kernel %{version}-%{release}.%{_target_cpu} || exit $?
fi

%post
%{_sbindir}/new-kernel-pkg --package %{name} --install %{version}-%{release}.%{_target_cpu} || exit $?

%preun
%{_sbindir}/new-kernel-pkg --rminitrd --rmmoddep --remove %{version}-%{release}.%{_target_cpu} || exit $?
if [ -x %{_sbindir}/weak-modules ]; then
    %{_sbindir}/weak-modules --remove-kernel %{version}-%{release}.%{_target_cpu} || exit $?
fi

%post devel
if [ -f /etc/sysconfig/kernel ]; then
    . /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ]; then
    pushd /usr/src/kernels/%{version}-%{release}.%{_target_cpu} > /dev/null
    /usr/bin/find . -type f | while read f; do
        /usr/sbin/hardlink -c /usr/src/kernels/*.fc*.*/$f $f
    done
    popd > /dev/null
fi
%endif

%if %{with_tools}
%post -n %{name}-tools
%{_sbindir}/ldconfig || exit $?

%postun -n %{name}-tools
%{_sbindir}/ldconfig || exit $?
%endif

# Files section.
%if %{with_default}
%files
%defattr(-,root,root)
/boot/vmlinuz-%{version}-%{release}.%{_target_cpu}
%attr(600,root,root) /boot/System.map-%{version}-%{release}.%{_target_cpu}
/boot/symvers-%{version}-%{release}.%{_target_cpu}.gz
/boot/config-%{version}-%{release}.%{_target_cpu}
%dir /lib/modules/%{version}-%{release}.%{_target_cpu}
/lib/modules/%{version}-%{release}.%{_target_cpu}/kernel
/lib/modules/%{version}-%{release}.%{_target_cpu}/build
/lib/modules/%{version}-%{release}.%{_target_cpu}/source
/lib/modules/%{version}-%{release}.%{_target_cpu}/extra
/lib/modules/%{version}-%{release}.%{_target_cpu}/updates
/lib/modules/%{version}-%{release}.%{_target_cpu}/weak-updates
%ifarch %{vdso_arches}
/lib/modules/%{version}-%{release}.%{_target_cpu}/vdso
/etc/ld.so.conf.d/%{name}-%{version}-%{release}.%{_target_cpu}.conf
%endif
/lib/modules/%{version}-%{release}.%{_target_cpu}/modules.*
%ghost /boot/initramfs-%{version}-%{release}.%{_target_cpu}.img

%files devel
%defattr(-,root,root)
/usr/src/kernels/%{version}-%{release}.%{_target_cpu}
%endif

%if %{with_headers}
%files headers
%defattr(-,root,root)
/usr/include/*
%endif

%if %{with_doc}
%files doc
%defattr(-,root,root)
%{_datadir}/doc/%{name}-doc-%{version}/Documentation/*
%dir %{_datadir}/doc/%{name}-doc-%{version}/Documentation
%dir %{_datadir}/doc/%{name}-doc-%{version}
%{_datadir}/man/man9/*
%endif

%if %{with_perf}
%files -n perf
%defattr(-,root,root)
%{_bindir}/perf
%{_bindir}/trace
%dir %{_libdir}/traceevent/plugins
%{_libdir}/traceevent/plugins/*
%dir %{_libexecdir}/perf-core
%{_libexecdir}/perf-core/*
%{_mandir}/man[1-8]/perf*
%dir %{_datadir}/perf-core
%{_datadir}/perf-core/*
%{_sysconfdir}/bash_completion.d/perf

%files -n python-perf
%defattr(-,root,root)
%{python_sitearch}
%endif

%if %{with_tools}
%files -n %{name}-tools -f cpupower.lang
%defattr(-,root,root)

%ifarch x86_64
%{_bindir}/cpupower
%{_bindir}/centrino-decode
%{_bindir}/powernow-k8-decode
%{_unitdir}/cpupower.service
%{_mandir}/man[1-8]/cpupower*
%config(noreplace) %{_sysconfdir}/sysconfig/cpupower
%{_bindir}/x86_energy_perf_policy
%{_mandir}/man8/x86_energy_perf_policy*
%{_bindir}/turbostat
%{_mandir}/man8/turbostat*

%files -n %{name}-tools-libs
%defattr(-,root,root)
%{_libdir}/libcpupower.so.0
%{_libdir}/libcpupower.so.0.0.0

%files -n %{name}-tools-libs-devel
%defattr(-,root,root)
%{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
%endif
%endif

%changelog
* Mon Nov 02 2015 Alan Bartlett <ajb@elrepo.org> - 4.3.0-1
- Updated with the 4.3 source tarball.

* Tue Oct 27 2015 Alan Bartlett <ajb@elrepo.org> - 4.2.5-1
- Updated with the 4.2.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.2.5]
- CONFIG_SCHEDSTATS=y [https://elrepo.org/bugs/view.php?id=603]

* Fri Oct 23 2015 Alan Bartlett <ajb@elrepo.org> - 4.2.4-1
- Updated with the 4.2.4 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.2.4]

* Sat Oct 03 2015 Alan Bartlett <ajb@elrepo.org> - 4.2.3-1
- Updated with the 4.2.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.2.3]

* Wed Sep 30 2015 Alan Bartlett <ajb@elrepo.org> - 4.2.2-1
- Updated with the 4.2.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.2.2]

* Mon Sep 21 2015 Alan Bartlett <ajb@elrepo.org> - 4.2.1-1
- Updated with the 4.2.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.2.1]
- CONFIG_BACKLIGHT_GPIO=m, CONFIG_BCMA_DRIVER_GPIO=y, CONFIG_CHARGER_GPIO=m,
- CONFIG_CHARGER_MANAGER=y, CONFIG_CLKDEV_LOOKUP=y, CONFIG_COMMON_CLK=y,
- CONFIG_EXTCON=y, CONFIG_GENERIC_IRQ_CHIP=y, CONFIG_GPIO_ACPI=y,
- CONFIG_GPIO_ADP5588=m, CONFIG_GPIO_AMD8111=m, CONFIG_GPIO_DEVRES=y,
- CONFIG_GPIO_DWAPB=m, CONFIG_GPIO_F7188X=m, CONFIG_GPIO_GENERIC=m,
- CONFIG_GPIO_GENERIC_PLATFORM=m, CONFIG_GPIO_ICH=m, CONFIG_GPIO_INTEL_MID=y,
- CONFIG_GPIO_IT8761E=m, CONFIG_GPIO_JANZ_TTL=m, CONFIG_GPIO_KEMPLD=m,
- CONFIG_GPIOLIB_IRQCHIP=y, CONFIG_GPIOLIB=y, CONFIG_GPIO_LP3943=m,
- CONFIG_GPIO_LYNXPOINT=m, CONFIG_GPIO_MAX7300=m, CONFIG_GPIO_MAX7301=m,
- CONFIG_GPIO_MAX730X=m, CONFIG_GPIO_MAX732X=m, CONFIG_GPIO_MC33880=m,
- CONFIG_GPIO_MCP23S08=m, CONFIG_GPIO_ML_IOH=m, CONFIG_GPIO_PCA953X=m,
- CONFIG_GPIO_PCF857X=m, CONFIG_GPIO_RDC321X=m, CONFIG_GPIO_SCH311X=m,
- CONFIG_GPIO_SCH=m, CONFIG_GPIO_SX150X=y, CONFIG_GPIO_SYSFS=y,
- CONFIG_GPIO_VX855=m, CONFIG_HAVE_CLK_PREPARE=y, CONFIG_HAVE_CLK=y,
- CONFIG_I2C_CBUS_GPIO=m, CONFIG_I2C_DESIGNWARE_PLATFORM=m, CONFIG_I2C_GPIO=m,
- CONFIG_I2C_MUX_GPIO=m, CONFIG_I2C_MUX_PCA954x=m, CONFIG_I2C_MUX_PINCTRL=m,
- CONFIG_LEDS_GPIO=m, CONFIG_LEDS_PCA9532_GPIO=y, CONFIG_LEDS_TRIGGER_GPIO=m,
- CONFIG_MDIO_GPIO=m, CONFIG_MFD_INTEL_QUARK_I2C_GPIO=m, CONFIG_MFD_SM501_GPIO=y,
- CONFIG_PINCTRL_BAYTRAIL=y, CONFIG_PINCTRL=y, CONFIG_PM_CLK=y,
- CONFIG_REGULATOR_GPIO=m, CONFIG_SENSORS_GPIO_FAN=m, CONFIG_SENSORS_SHT15=m,
- CONFIG_SND_COMPRESS_OFFLOAD=m, CONFIG_SND_DESIGNWARE_I2S=m,
- CONFIG_SND_DMAENGINE_PCM=m, CONFIG_SND_SOC_GENERIC_DMAENGINE_PCM=y,
- CONFIG_SND_SOC_I2C_AND_SPI=m, CONFIG_SND_SOC=m, CONFIG_SPI_GPIO=m,
- CONFIG_SPI_PXA2XX_DMA=y, CONFIG_SPI_PXA2XX=m, CONFIG_SPI_PXA2XX_PCI=m,
- CONFIG_SSB_DRIVER_GPIO=y, CONFIG_USB_DWC3_DUAL_ROLE=y, CONFIG_USB_F_MASS_STORAGE=m,
- CONFIG_USB_GADGET=m, CONFIG_USB_GADGET_STORAGE_NUM_BUFFERS=2,
- CONFIG_USB_GADGET_VBUS_DRAW=2, CONFIG_USB_LIBCOMPOSITE=m,
- CONFIG_USB_MASS_STORAGE=m and CONFIG_X86_INTEL_LPSS=y
- [https://elrepo.org/bugs/view.php?id=592]

* Mon Aug 31 2015 Alan Bartlett <ajb@elrepo.org> - 4.2.0-1
- Updated with the 4.2 source tarball.

* Mon Aug 17 2015 Alan Bartlett <ajb@elrepo.org> - 4.1.6-1
- Updated with the 4.1.6 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.1.6]

* Tue Aug 11 2015 Alan Bartlett <ajb@elrepo.org> - 4.1.5-1
- Updated with the 4.1.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.1.5]

* Wed Aug 05 2015 Alan Bartlett <ajb@elrepo.org> - 4.1.4-1
- Updated with the 4.1.4 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.1.4]

* Wed Jul 22 2015 Alan Bartlett <ajb@elrepo.org> - 4.1.3-1
- Updated with the 4.1.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.1.3]

* Sat Jul 11 2015 Alan Bartlett <ajb@elrepo.org> - 4.1.2-1
- Updated with the 4.1.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.1.2]

* Mon Jun 29 2015 Alan Bartlett <ajb@elrepo.org> - 4.1.1-1
- Updated with the 4.1.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.1.1]
- CONFIG_BLK_DEV_DRBD=m [https://elrepo.org/bugs/view.php?id=575]

* Mon Jun 22 2015 Alan Bartlett <ajb@elrepo.org> - 4.1.0-1
- Updated with the 4.1 source tarball.
- CONFIG_BRIDGE_NETFILTER=y [https://elrepo.org/bugs/view.php?id=573]

* Sun Jun 07 2015 Alan Bartlett <ajb@elrepo.org> - 4.0.5-1
- Updated with the 4.0.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.0.5]

* Sun May 17 2015 Alan Bartlett <ajb@elrepo.org> - 4.0.4-1
- Updated with the 4.0.4 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.0.4]

* Wed May 13 2015 Alan Bartlett <ajb@elrepo.org> - 4.0.3-1
- Updated with the 4.0.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.0.3]

* Thu May 07 2015 Alan Bartlett <ajb@elrepo.org> - 4.0.2-1
- Updated with the 4.0.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.0.2]

* Thu Apr 30 2015 Alan Bartlett <ajb@elrepo.org> - 4.0.1-1
- Updated with the 4.0.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v4.x/ChangeLog-4.0.1]

* Mon Apr 13 2015 Alan Bartlett <ajb@elrepo.org> - 4.0.0-1
- Updated with the 4.0 source tarball.

* Thu Mar 26 2015 Alan Bartlett <ajb@elrepo.org> - 3.19.3-1
- Updated with the 3.19.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.19.3]

* Wed Mar 18 2015 Alan Bartlett <ajb@elrepo.org> - 3.19.2-1
- Updated with the 3.19.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.19.2]

* Sat Mar 07 2015 Alan Bartlett <ajb@elrepo.org> - 3.19.1-1
- Updated with the 3.19.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.19.1]

* Mon Feb 09 2015 Alan Bartlett <ajb@elrepo.org> - 3.19.0-1
- Updated with the 3.19 source tarball.

* Fri Feb 06 2015 Alan Bartlett <ajb@elrepo.org> - 3.18.6-1
- Updated with the 3.18.6 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.18.6]

* Fri Jan 30 2015 Alan Bartlett <ajb@elrepo.org> - 3.18.5-1
- Updated with the 3.18.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.18.5]

* Wed Jan 28 2015 Alan Bartlett <ajb@elrepo.org> - 3.18.4-1
- Updated with the 3.18.4 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.18.4]
- CONFIG_THUNDERBOLT=m [http://lists.elrepo.org/pipermail/elrepo/2015-January/002516.html]
- CONFIG_OVERLAY_FS=m [https://elrepo.org/bugs/view.php?id=548]

* Fri Jan 16 2015 Alan Bartlett <ajb@elrepo.org> - 3.18.3-1
- Updated with the 3.18.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.18.3]

* Fri Jan 09 2015 Alan Bartlett <ajb@elrepo.org> - 3.18.2-1
- Updated with the 3.18.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.18.2]

* Tue Dec 16 2014 Alan Bartlett <ajb@elrepo.org> - 3.18.1-1
- Updated with the 3.18.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.18.1]

* Mon Dec 08 2014 Alan Bartlett <ajb@elrepo.org> - 3.18.0-1
- Updated with the 3.18 source tarball.

* Mon Dec 08 2014 Alan Bartlett <ajb@elrepo.org> - 3.17.6-1
- Updated with the 3.17.6 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.17.6]

* Sun Dec 07 2014 Alan Bartlett <ajb@elrepo.org> - 3.17.5-1
- Updated with the 3.17.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.17.5]

* Sun Nov 30 2014 Alan Bartlett <ajb@elrepo,org> - 3.17.4-2
- CONFIG_BLK_DEV_NBD=m [https://elrepo.org/bugs/view.php?id=538]

* Sat Nov 22 2014 Alan Bartlett <ajb@elrepo.org> - 3.17.4-1
- Updated with the 3.17.4 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.17.4]
- CONFIG_CHROME_PLATFORMS=y, CONFIG_CHROMEOS_LAPTOP=m and
- CONFIG_CHROMEOS_PSTORE=m [https://elrepo.org/bugs/view.php?id=532]

* Sat Nov 15 2014 Alan Bartlett <ajb@elrepo.org> - 3.17.3-1
- Updated with the 3.17.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.17.3]
- CONFIG_BLK_DEV_RBD=m [https://elrepo.org/bugs/view.php?id=521]

* Fri Oct 31 2014 Alan Bartlett <ajb@elrepo.org> - 3.17.2-1
- Updated with the 3.17.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.17.2]

* Wed Oct 15 2014 Alan Bartlett <ajb@elrepo.org> - 3.17.1-1
- Updated with the 3.17.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.17.1]

* Mon Oct 06 2014 Alan Bartlett <ajb@elrepo.org> - 3.17.0-1
- Updated with the 3.17 source tarball.
- CONFIG_9P_FS=m, CONFIG_9P_FSCACHE=y and CONFIG_9P_FS_POSIX_ACL=y
- [https://elrepo.org/bugs/view.php?id=510]

* Thu Sep 18 2014 Alan Bartlett <ajb@elrepo.org> - 3.16.3-1
- Updated with the 3.16.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.16.3]

* Sat Sep 06 2014 Alan Bartlett <ajb@elrepo.org> - 3.16.2-1
- Updated with the 3.16.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.16.2]

* Thu Aug 14 2014 Alan Bartlett <ajb@elrepo.org> - 3.16.1-1
- Updated with the 3.16.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.16.1]
- CONFIG_ATH9K_DEBUGFS=y, CONFIG_ATH9K_HTC_DEBUGFS=y &
- CONFIG_ATH10K_DEBUGFS=y [https://elrepo.org/bugs/view.php?id=501]

* Mon Aug 04 2014 Alan Bartlett <ajb@elrepo.org> - 3.16.0-1
- Updated with the 3.16 source tarball.
- CONFIG_XEN_PCIDEV_BACKEND=y & CONFIG_XEN_FBDEV_FRONTEND=m [Mark Pryor]

* Fri Aug 01 2014 Alan Bartlett <ajb@elrepo.org> - 3.15.8-1
- Updated with the 3.15.8 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.15.8]

* Mon Jul 28 2014 Alan Bartlett <ajb@elrepo.org> - 3.15.7-1
- Updated with the 3.15.7 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.15.7]

* Fri Jul 18 2014 Alan Bartlett <ajb@elrepo.org> - 3.15.6-1
- Updated with the 3.15.6 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.15.6]

* Thu Jul 10 2014 Alan Bartlett <ajb@elrepo.org> - 3.15.5-1
- Updated with the 3.15.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.15.5]

* Mon Jul 07 2014 Alan Bartlett <ajb@elrepo.org> - 3.15.4-1
- Updated with the 3.15.4 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.15.4]

* Tue Jul 01 2014 Alan Bartlett <ajb@elrepo.org> - 3.15.3-1
- Updated with the 3.15.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.15.3]

* Fri Jun 27 2014 Alan Bartlett <ajb@elrepo.org> - 3.15.2-1
- Updated with the 3.15.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.15.2]

* Tue Jun 17 2014 Alan Bartlett <ajb@elrepo.org> - 3.15.1-1
- Updated with the 3.15.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.15.1]

* Thu Jun 12 2014 Alan Bartlett <ajb@elrepo.org> - 3.15.0-1
- General availability.

* Sun Jun 08 2014 Alan Bartlett <ajb@elrepo.org> - 3.15.0-0.rc8
- Updated with the 3.15 source tarball.
- The eighth release candidate of a kernel-ml-aufs package set for EL7.

* Sun Jun 08 2014 Alan Bartlett <ajb@elrepo.org> - 3.14.6-0.rc7
- Updated with the 3.14.6 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.14.6]
- The seventh release candidate of a kernel-ml-aufs package set for EL7.

* Wed Jun 04 2014 Alan Bartlett <ajb@elrepo.org> - 3.14.5-0.rc6
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.14.5]
- The sixth release candidate of a kernel-ml-aufs package set for EL7.
- Added a "Conflicts:" line for the kernel-ml-aufs-doc package.

* Mon Jun 02 2014 Alan Bartlett <ajb@elrepo.org> - 3.14.5-0.rc5
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.14.5]
- The fifth release candidate of a kernel-ml-aufs package set for EL7.
- CONFIG_SECURITY_TOMOYO_ACTIVATION_TRIGGER="/usr/lib/systemd/systemd"
- Corrected the "Conflicts:" line for the kernel-ml-aufs-tools-libs-devel
- package. [Akemi Yagi]

* Sun Jun 01 2014 Alan Bartlett <ajb@elrepo.org> - 3.14.5-0.rc4
- Updated with the 3.14.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.14.5]
- The fourth release candidate of a kernel-ml-aufs package set for EL7.
- Added a "Conflicts:" line for the kernel-ml-aufs-tools,
- kernel-ml-aufs-tools-libs & kernel-ml-aufs-tools-devel packages.

* Wed May 28 2014 Alan Bartlett <ajb@elrepo.org> - 3.14.4-0.rc3
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.14.4]
- The third release candidate of a kernel-ml-aufs package set for EL7.
- Fix a problem with the symlink between the /usr/src/$(uname -r)/
- directory and the /lib/modules/$(uname -r)/build directory.

* Sat May 24 2014 Alan Bartlett <ajb@elrepo.org> - 3.14.4-0.rc2
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.14.4]
- The second release candidate of a kernel-ml-aufs package set for EL7.
- Add calls of weak-modules to the %%posttrans & %%preun scripts.

* Tue May 20 2014 Alan Bartlett <ajb@elrepo.org> - 3.14.4-0.rc1
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.14.4]
- Skip the beta phase.
- The first release candidate of a kernel-ml-aufs package set for EL7.

* Mon May 19 2014 Alan Bartlett <ajb@elrepo.org> - 3.14.4-0.alpha3
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.14.4]
- The third attempt to build a kernel-ml-aufs package set for EL7.

* Sun May 18 2014 Alan Bartlett <ajb@elrepo.org> - 3.14.4-0.alpha2
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.14.4]
- The second attempt to build a kernel-ml-aufs package set for EL7.

* Sat May 17 2014 Alan Bartlett <ajb@elrepo.org> - 3.14.4-0.alpha1
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.14.4]
- The first attempt to build a kernel-ml-aufs package set for EL7.
