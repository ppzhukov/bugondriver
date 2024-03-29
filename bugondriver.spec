# norootforbuild

# The following line tells the buildservice to save the project certificate as
# %_sourcedir/_projectcert.crt
# needssslcertforbuild

Name:           bugondriver
Version:                1.0
Release:                0
Summary:                BUGON Kernel Module Package
License:                GPL-3.0
Url:          https://github.com/ppzhukov/bugondriver
Group:          System/Kernel
Source0:                %{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%if 0%{?fedora}%{?rhel}&&!0%{?centos_version} == 700&&!0%{?rhel_version} == 700
BuildRequires:  redhat-rpm-config kernel-rpm-macros elfutils-libelf-devel kmod
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-devel
%endif

%if 0%{?sle_version}||0%{?centos_version} == 700||0%{?rhel_version} == 700
BuildRequires:  %{?kernel_module_package_buildreqs}
BuildRequires:  pesign-obs-integration
%endif

%if 0%{?sle_version}||0%{?centos_version} == 700||0%{?rhel_version} == 700
%kernel_module_package -x debug -x trace -c %_sourcedir/_projectcert.crt 
%endif

%description
This package contains the bugondriver.ko module.

%prep
%setup
set -- *
mkdir source
mv "$@" source/
mkdir obj

%if 0%{?fedora}%{?rhel}&&!0%{?centos_version} == 700&&!0%{?rhel_version} == 700
%build
for flavor in %flavors_to_build; do
    rm -rf obj/$flavor
    cp -r source obj/$flavor
    make -C /lib/modules/$(uname -r)/build M=$PWD/obj/$flavor
done
%install
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=extra
for flavor in %flavors_to_build; do
       make -C /lib/modules/$(uname -r)/build modules_install M=$PWD/obj/$flavor
done
%endif

%if 0%{?sle_version}||0%{?centos_version} == 700||0%{?rhel_version} == 700
%build
for flavor in %flavors_to_build; do
       rm -rf obj/$flavor
       cp -r source obj/$flavor
       make -C %{kernel_source $flavor} modules M=$PWD/obj/$flavor
done
%install
# The BRP_PESIGN_FILES variable must be set to a space separated list of
# directories or patterns matching files that need to be signed.  E.g., packages
# that include firmware files would set BRP_PESIGN_FILES='*.ko /lib/firmware'
export BRP_PESIGN_FILES='*.ko'

export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=extra
for flavor in %flavors_to_build; do
       make -C %{kernel_source $flavor} modules_install M=$PWD/obj/$flavor
done
%endif

%changelog
* Wed Jan 31 2024 Pavel Zhukov <pp.zhukov@gmail.com>
- Added signing phase for kernel modules to support UEFI secure boot in SUSE.
* Sun Jan 21 2024 Pavel Zhukov <pp.zhukov@gmail.com>
- Added support for CentOS/Fedora.
* Thu Jan 18 2024 Pavel Zhukov <pp.zhukov@gmail.com>
- First build.

