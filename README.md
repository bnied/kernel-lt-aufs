NOTE: This is a work-in-progress to get AUFS building against kernel-ml 3.16.1. Breakage should be expected.
=============================================================================

This repository contains the specfile and config files to build [kernel-ml](http://elrepo.org/tiki/kernel-ml) kernels that include AUFS for use with Docker. The Docker spec files are part of the original repo this was forked from, and should be considered outdated. Use Docker from [EPEL](https://admin.fedoraproject.org/pkgdb/acls/name/docker-io) instead.

Before building the packages, be sure to install [fedora-packager](https://dl.fedoraproject.org/pub/epel/6/x86_64/repoview/fedora-packager.html) and add yourself to the _mock_ group.

You can build the packages with the following commands. Note that building the kernel can take a long time, possibly even several hours. If you want to build these for Fedora instead of RHEL, when running mock you should replace epel-6-x86\_64 with fedora-19-x86\_64. 

**NOTE**: `9929e444955f467073ebedf254a9ac0f7a5df1c5` was the latest commit of the `aufs3.16` branch at the time of this writing. When you build your kernel versions, feel free to update this step to the latest commit.

    # build kernel rpm
    
    spectool -g -C kernel-ml-aufs kernel-ml-aufs/kernel-ml-aufs-3.16.spec 
    git clone git://git.code.sf.net/p/aufs/aufs3-standalone -b aufs3.16
    pushd aufs3-standalone
    git archive 53c6c3305f8a17b5911f960a8788edf98392e0ed > ../kernel-ml-aufs/aufs3-standalone.tar
    popd
    mock -r epel-6-x86_64 --buildsrpm --spec kernel-ml-aufs/kernel-ml-aufs-3.16.spec --sources kernel-ml-aufs --resultdir output
    mock -r epel-6-x86_64 --rebuild --resultdir output output/kernel-ml-aufs-3.16.1-1.el6.src.rpm

The resulting RPMs will be placed in a directory named _output_. You can install them with

    cd output
    yum localinstall --nogpgcheck kernel-ml-aufs-3.10.11-1.el6.x86_64.rpm
In order to use docker, you'll need to install it out of EPEL:

    yum install docker
You'll need to configure the cgroup filesystem and reboot into your new kernel. Add the line

    none                    /sys/fs/cgroup          cgroup  defaults        0 0

to _/etc/fstab_. Reboot and choose the 3.xx kernel from your GRUB menu (or edit _/boot/grub/grub.conf_ and change your default kernel).

The docker daemon should have started automatically; this can be controlled by via [initctl](http://upstart.ubuntu.com/cookbook/#initctl). To give a non-root user permission to use docker, add them to the _docker_ group.
