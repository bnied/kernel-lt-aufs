#!/usr/bin/env bash

# rhel-aufs-kernel builder
# This script automates building out the latest kernel-ml package with AUFS support

# Get the kernel version to build
echo "What kernel version do you want to build? (major version only)"
read VERSION

# Get the architecture to build
echo "What architecture do you want to build for? (i686, i686-NONPAE, x86_64)"
read ARCH

# Get version of CentOS/RHEL to build for
echo "What version of CentOS/RHEL do you want to build for? (6 or 7)"
read EL_VERSION

# If our spec file is missing, exit
if [ ! -f kernel-ml-aufs/kernel-ml-aufs-$VERSION.spec ]; then
	echo "Spec file not found for version $VERSION"
	exit 1
fi

# Get minor config version from spec file
FULL_VERSION=`cat kernel-ml-aufs/kernel-ml-aufs-$VERSION.spec | grep "%define LKAver" | awk '{print $3}'`

# If we only have two parts to our version number, append ".0" to the end
VERSION_ARRAY=(`echo $FULL_VERSION | tr "." "\n"`)
if [ ${#VERSION_ARRAY[@]} -le 2 ]; then
	FULL_VERSION="$FULL_VERSION.0"
fi

# If our kernel config is missing, exit
if [ ! -f kernel-ml-aufs/config-$FULL_VERSION-$ARCH ]; then
	echo "Config file not found for $FULL_VERSION-$ARCH"
	exit 1
fi

# Copy everything to a temp directory
echo "Creating temp directory..."
mkdir temp
echo "Creating log directory..."
mkdir temp/logs
echo "Copying files to temp directory..."
cp -a kernel-ml-aufs temp/

# From hereon out, everything we do will be in the temp directory
cd temp

# Grab the source files for our kernel version
echo "Grabbing kernel source..."
spectool -g -C kernel-ml-aufs kernel-ml-aufs/kernel-ml-aufs-$VERSION.spec > logs/spectool.log 2>&1

# Clone the AUFS repo
git clone git://git.code.sf.net/p/aufs/aufs3-standalone -b aufs$VERSION > logs/aufs-git.log 2>&1

# Get the HEAD commit from the aufs tree
echo "Cloning AUFS source into our kernel sources..."
pushd aufs3-standalone
HEAD_COMMIT=`git rev-parse --short HEAD 2> /dev/null`
git archive $HEAD_COMMIT > ../kernel-ml-aufs/aufs3-standalone.tar
popd

# Create our SRPM
echo "Creating source RPM..."
mock -r epel-$EL_VERSION-x86_64 --buildsrpm --spec kernel-ml-aufs/kernel-ml-aufs-$VERSION.spec --sources kernel-ml-aufs --resultdir output > logs/srpm_generation.log 2>&1

# If successful, create our binary RPMs
if [ $? -eq 0 ]; then
	echo "Source RPM created. Building binary RPMs..."
	mock -r epel-$EL_VERSION-x86_64 --rebuild --resultdir output output/kernel-ml-aufs-$FULL_VERSION-1.el$EL_VERSION.src.rpm > logs/rpm_generation.log 2>&1
fi

if [ $? -eq 0 ]; then
	mkdir ~/RPMs
	echo "Binary RPMs created successfully! Moving to ~/RPMs"
	mv output/*.rpm ~/RPMs
	echo "Removing temp directory..."
	rm -rf temp
else
	echo "Binary RPM creation failed! See logs for details."
fi


