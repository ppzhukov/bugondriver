#norootforbuild

Name:           bugondriver
Version:                1.0
Release:                0
Summary:                BUGON Kernel Module Package
License:                GPL-3.0
Url:          https://github.com/ppzhukov/bugondriver
Group:          System/Kernel
Source0:                %{name}-%{version}.tar.xz

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%if 0%{?fedora}%{?rhel}&&!0%{?centos_version} == 700
BuildRequires:  redhat-rpm-config kernel-rpm-macros elfutils-libelf-devel kmod
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-devel
%endif

%if 0%{?sle_version}||0%{?centos_version} == 700
%kernel_module_package
BuildRequires:  %{kernel_module_package_buildreqs}
%endif

%description
This package contains the bugondriver.ko module.

%prep
%setup
set -- *
mkdir source
mv "$@" source/
mkdir obj

%build
for flavor in %flavors_to_build; do
       rm -rf obj/$flavor
       cp -r source obj/$flavor
       make -C %{kernel_source $flavor} modules M=$PWD/obj/$flavor
done

%install
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=extra
for flavor in %flavors_to_build; do
       make -C %{kernel_source $flavor} modules_install M=$PWD/obj/$flavor
done

%changelog

* Fri Jan 19 2024 Pavel Zhukov <pp.zhukov@gmail.com>
- First build