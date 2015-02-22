RHEL-AUFS-Kernel: `kernel-ml` with AUFS Support
=============================================================================

This repository contains the specfile and config files to build [kernel-ml](http://elrepo.org/tiki/kernel-ml) kernels that include AUFS for use with Docker. The Docker spec files that were part of the original repo are no longer included. Use Docker from [EPEL](https://admin.fedoraproject.org/pkgdb/acls/name/docker-io) instead.

Before building the packages, be sure to install [fedora-packager](https://dl.fedoraproject.org/pub/epel/6/x86_64/repoview/fedora-packager.html) and add yourself to the _mock_ group.

Be aware that building the kernel can take a long time (at least half an hour, up to several hours if you're building on an older machine).

To build the packages, there are two options:

Run the `build_kernel.sh` script, and answer all three questions. This will automate the build:

    $ ./build_kernel.sh 
    What kernel version do you want to build? (major version only)
    3.19
    What architecture do you want to build for? (i686, i686-NONPAE, x86_64)
    x86_64
    What version of CentOS/RHEL do you want to build for? (6 or 7)
    7

If you'd rather run through the steps manually, you can do so with the instructions below. Be sure to change `epel-6-x86_64` to `epel-7-x86_64` and the filename for the source RPM if you're building for EL7.

Additionally,  `f60288dc0e0aab77ca545f42d785ec280f4700b9` was the latest commit of the `aufs3.19` branch at the time of this writing. When you build your kernel versions, be sure to update this step to the latest commit.
    
    spectool -g -C kernel-ml-aufs kernel-ml-aufs/kernel-ml-aufs-3.19.spec
    git clone git://git.code.sf.net/p/aufs/aufs3-standalone -b aufs3.19
    pushd aufs3-standalone
    git archive f60288dc0e0aab77ca545f42d785ec280f4700b9 > ../kernel-ml-aufs/aufs3-standalone.tar
    popd
    mock -r epel-6-x86_64 --buildsrpm --spec kernel-ml-aufs/kernel-ml-aufs-3.19.spec --sources kernel-ml-aufs --resultdir output
    mock -r epel-6-x86_64 --rebuild --resultdir output output/kernel-ml-aufs-3.19.0-1.el6.src.rpm

The resulting RPMs will be placed in a directory named _output_. You can install them with

    cd output
    yum localinstall --nogpgcheck kernel-ml-aufs-3.19.0-1.el6.x86_64.rpm

In order to use docker, you'll need to install it out of EPEL:

    yum install docker-io

Reboot and choose the 3.xx kernel from your GRUB menu (or edit _/boot/grub/grub.conf_ and change your default kernel).
