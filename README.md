# `kernel-lt-aufs`: `kernel-lt` with AUFS Support

This repository contains the RPM spec and config files to build [kernel-lt](http://elrepo.org/tiki/kernel-lt) kernels that include [the AUFS filesystem](http://aufs.sourceforge.net).

The Docker spec files that were part of the [original repo](https://github.com/sciurus/docker-rhel-rpm.git) are no longer included.

Additionally, the build script I had written to build these RPMs has been deprecated. RPM building is now done via the [`kernel-lt-aufs-docker` image.](https://github.com/bnied/kernel-lt-aufs-docker)

This has been tested on the following distributions:
* CentOS 7
* CentOS 8
* Red Hat Enterprise Linux 7
* Red Hat Enterprise Linux 8

Other RHEL-derivative Linux distributions (AlmaLinux, Rocky Linux, etc.) should all work as well, but haven't been tested.

### EL6 support has ended. However, older kernel packages are available on `yum.spaceduck.org` for historical purposes.

***
## Downloading Packages

Packages are available from [the Spaceduck.org Yum repo](https://yum.spaceduck.org/). Install the [.repo](https://yum.spaceduck.org/kernel-lt-aufs/kernel-lt-aufs.repo) file into `/etc/yum.repos.d` to get updates automatically.

**If you want these packages to be your default kernel in GRUB:** edit `/etc/sysconfig/kernel`, and change `DEFAULTKERNEL` to:
* `DEFAULTKERNEL=kernel-lt-aufs` for EL7
* `DEFAULTKERNEL=kernel-lt-aufs-core` for EL8
