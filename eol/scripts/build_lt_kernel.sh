#!/usr/bin/env bash

# rhel-aufs-kernel builder
# This script automates building out the latest kernel-lt package with AUFS support

# Start by seeing how many command line arguments we were passed
for i in "$@"; do
  case $i in
    -v=*|--version=*)
    VERSION="${i#*=}"
    ;;
    -a=*|--arch=*)
    ARCH="${i#*=}"
    ;;
    -e=*|--elversion=*)
    EL_VERSION="${i#*=}"
    ;;
    -s|--srpm-only)
    SRPM_ONLY=true
    ;;
    -h|--help)
    echo "usage: -v=<kernel_version> -a=<architecture> -e=<el_version>"
    exit 1
    ;;
  esac
done

# If we weren't passed these variables as commandline options, ask for them
if [ -z "$VERSION" ]; then
  # Get the kernel version to build
  echo "Kernel version not specified. What kernel version do you want to build? (major version only)"
  read VERSION
fi

if [ -z "$ARCH" ]; then
  # Get the architecture to build
  echo "Architecture not specified. What architecture do you want to build for? (i686, i686-NONPAE, x86_64)"
  read ARCH
fi

if [ -z "$EL_VERSION" ]; then
  # Get version of CentOS/RHEL to build for
  echo "EL Version not specified. What version of CentOS/RHEL do you want to build for? (6 or 7)"
  read EL_VERSION
fi

# Set the EL version tag for the RPMs
RPM_EL_VERSION="el${EL_VERSION}"

# Set the EL arch for mock
if [ $ARCH == "i686" ]; then
  MOCK_ARCH="i386"
else
  MOCK_ARCH=$ARCH
fi

# If our spec file is missing, exit
if [ ! -f ../specs-el$EL_VERSION/kernel-lt-aufs-$VERSION.spec ]; then
  echo "Spec file not found for version $VERSION"
  exit 1
fi

# Get minor config version from spec file
FULL_VERSION=`cat ../specs-el$EL_VERSION/kernel-lt-aufs-$VERSION.spec | grep "%define LKAver" | awk '{print $3}'`

# If we only have two parts to our version number, append ".0" to the end
VERSION_ARRAY=(`echo $FULL_VERSION | tr "." "\n"`)
if [ ${#VERSION_ARRAY[@]} -le 2 ]; then
  FULL_VERSION="$FULL_VERSION.0"
fi

# If our kernel config is missing, exit
if [ ! -f ../configs-el$EL_VERSION/config-$FULL_VERSION-$ARCH ]; then
  echo "Config file not found for $FULL_VERSION-$ARCH"
  exit 1
fi

# Announce what we've been asked to build LOUDLY
printf "*********** KERNEL-LT-AUFS BUILD COMMENCING ***********"
printf "\n\n\t* Version:\t$FULL_VERSION"
printf "\n\t* Architecture:\t$ARCH"
printf "\n\t* EL Version:\t$EL_VERSION"
printf "\n\n*******************************************************\n\n"

# See if we already have a build directory; if we do, nuke it
if [ -d "build" ]; then
  echo "Build directory found! Removing..."
  rm -rf ./build
fi

# Create a build directory with all the stuff we need
echo "Creating build directory..."
mkdir -p build/logs
mkdir -p build/rpms
echo "Copying spec file and config file(s) to build directory..."
cp -a ../specs-el$EL_VERSION/kernel-lt-aufs-$VERSION.spec build/kernel-lt-aufs.spec
cp -a ../configs-el$EL_VERSION/config-$FULL_VERSION-* build/
if [ $EL_VERSION -ne 6 ]; then
  cp -a ../configs-el7/cpupower* build
fi

# From hereon out, everything we do will be in the temp directory
cd build

# Grab the source files for our kernel version
echo "Grabbing kernel source..."
spectool -g -C . kernel-lt-aufs.spec > logs/spectool.log 2>&1

# Clone the AUFS repo
if [[ $VERSION =~ ^4 ]]; then
  echo "Cloning AUFS 4.x..."
  if [[ $VERSION == "4.19" ]]; then
    echo "Cloning AUFS 4.19.17+..."
    git clone git://github.com/sfjro/aufs4-standalone.git -b aufs4.19.17+ aufs-standalone > logs/aufs-git.log 2>&1
  else
    echo "Cloning AUFS 4.x normally..."
    git clone git://github.com/sfjro/aufs4-standalone.git -b aufs$VERSION aufs-standalone > logs/aufs-git.log 2>&1
  fi
else
  echo "Cloning AUFS 3.x..."
  git clone git://git.code.sf.net/p/aufs/aufs3-standalone -b aufs$VERSION aufs-standalone > logs/aufs-git.log 2>&1
fi

# Get the HEAD commit from the aufs tree
echo "Creating AUFS source tarball for packaging..."
pushd aufs-standalone 2>&1 > /dev/null
HEAD_COMMIT=`git rev-parse --short HEAD 2> /dev/null`
git archive $HEAD_COMMIT > ../aufs-standalone.tar
popd 2>&1 > /dev/null
rm -rf aufs-standalone

# Select our mock config
if [ $EL_VERSION -eq 8 ]; then
  MOCK_CONFIG="rhelbeta-8-${MOCK_ARCH}"
else
  MOCK_CONFIG="epel-${EL_VERSION}-${MOCK_ARCH}"
fi

# Create our SRPM
echo "Creating source RPM..."
mock -r $MOCK_CONFIG --buildsrpm --spec kernel-lt-aufs.spec --sources . --resultdir rpms > logs/srpm_generation.log 2>&1

# If we built the SRPM successfully, report that
if [ $? -eq 0 ]; then
  echo "Source RPM created."
else
  echo "Could not create source RPM! Exiting!"
  exit 1
fi

# Only build our binary RPMs if we didn't specify SRPM_ONLY
if [ -z "$SRPM_ONLY" ]; then
  echo "Building binary RPMs..."
  mock -r $MOCK_CONFIG --rebuild --resultdir rpms rpms/kernel-lt-aufs-$FULL_VERSION-1.$RPM_EL_VERSION.src.rpm > logs/rpm_generation.log 2>&1
  if [ $? -eq 0 ]; then
    echo "RPMs created successfully!"
  else
    echo "RPMs were not created successfully! See log for details."
    exit 1
  fi
fi

# If we built the RPMs successfully, report that
if [ $? -eq 0 ]; then
  # Now that we've tested the source RPM, we can submit it to copr
  echo "Submitting build to Copr..."
  copr-cli build kernel-lt-aufs --nowait -r $MOCK_CONFIG rpms/kernel-lt-aufs-$FULL_VERSION-1.$RPM_EL_VERSION.src.rpm > logs/copr_submission.log 2>&1
  if [ $? -eq 0 ]; then
    echo "Submitted to Copr successfully!"
  else
    echo "Submitted to Copr failed! See log for details."
  fi
  if [ ! -d ~/RPMs/lt ]; then
    echo "Creating RPM directory..."
    mkdir -p ~/RPMs/lt 2>&1
  fi
  echo "Moving to ~/RPMs/lt..."
  mv rpms/*.rpm ~/RPMs/lt
  echo "Exiting..."
  exit 0
else
  echo "Binary RPM creation failed! See logs for details."
  exit 1
fi
