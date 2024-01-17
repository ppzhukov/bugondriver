#norootforbuild

Name:			bugondriver
BuildRequires:	%kernel_module_package_buildreqs
License:		GPL
Group:			System/Kernel
Summary:		BUGON Driver
Version:		1.0
Release:		0
Source0:		%name-%version.tar.bz2
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%kernel_module_package

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
export INSTALL_MOD_DIR=updates
for flavor in %flavors_to_build; do
        make -C %{kernel_source $flavor} modules_install M=$PWD/obj/$flavor
done

%changelog
