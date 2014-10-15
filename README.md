RHEL-AUFS-Kernel: `kernel-ml` with AUFS Support
=============================================================================

This repository contains the specfile and config files to build [kernel-ml](http://elrepo.org/tiki/kernel-ml) kernels that include AUFS for use with Docker. The Docker spec files that were part of the original repo are no longer included. Use Docker from [EPEL](https://admin.fedoraproject.org/pkgdb/acls/name/docker-io) instead.

Before building the packages, be sure to install [fedora-packager](https://dl.fedoraproject.org/pub/epel/6/x86_64/repoview/fedora-packager.html) and add yourself to the _mock_ group.

These packages can be built using the following commands. Be aware that building the kernel can take a long time (at least half an hour, up to several hours if you're building on an older machine). If you want to build these for RHEL/CentOS 7, change `epel-6-x86_64` to `epel-7-x86_64` in the instructions below, and make sure that you change the filename for the source RPM to the EL7 equivalent.

**NOTE**: `fe1e5d50b83e2987676c27f3e9f721d382e5fefc` was the latest commit of the `aufs3.17` branch at the time of this writing. When you build your kernel versions, feel free to update this step to the latest commit.

    # build kernel rpm

    spectool -g -C kernel-ml-aufs kernel-ml-aufs/kernel-ml-aufs-3.17.spec
    git clone git://git.code.sf.net/p/aufs/aufs3-standalone -b aufs3.17
    pushd aufs3-standalone
    git archive fe1e5d50b83e2987676c27f3e9f721d382e5fefc > ../kernel-ml-aufs/aufs3-standalone.tar
    popd
    mock -r epel-6-x86_64 --buildsrpm --spec kernel-ml-aufs/kernel-ml-aufs-3.17.spec --sources kernel-ml-aufs --resultdir output
    mock -r epel-6-x86_64 --rebuild --resultdir output output/kernel-ml-aufs-3.17.1-1.el6.src.rpm

The resulting RPMs will be placed in a directory named _output_. You can install them with

    cd output
    yum localinstall --nogpgcheck kernel-ml-aufs-3.17.1-1.el6.x86_64.rpm
In order to use docker, you'll need to install it out of EPEL:

    yum install docker-io
You'll need to configure the cgroup filesystem and reboot into your new kernel. Add the line

    none                    /sys/fs/cgroup          cgroup  defaults        0 0

to _/etc/fstab_. Reboot and choose the 3.xx kernel from your GRUB menu (or edit _/boot/grub/grub.conf_ and change your default kernel).
