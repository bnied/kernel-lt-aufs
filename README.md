# `kernel-lt-aufs`: `kernel-lt` with AUFS Support

This repository contains the RPM spec and config files to build [kernel-lt](http://elrepo.org/tiki/kernel-lt) kernels that include [the AUFS filesystem](http://aufs.sourceforge.net).

The Docker spec files that were part of the [original repo](https://github.com/sciurus/docker-rhel-rpm.git) are no longer included.

These kernels should work on Red Hat Enterprise Linux, and any RHEL-derivative distrubition, such Almalinux, CentOS, Oracle Enterprise Linux, or Rocky Linux.

***
## Downloading Packages

Packages are available from [Copr](https://copr.fedorainfracloud.org/coprs/bnied/kernel-lt-aufs). Follow the instructions there to get updates automatically.

**If you want these packages to be your default kernel in GRUB:** edit `/etc/sysconfig/kernel`, and change `DEFAULTKERNEL` to:
* `DEFAULTKERNEL=kernel-lt-aufs` for EL7
* `DEFAULTKERNEL=kernel-lt-aufs-core` for EL8/EL9
