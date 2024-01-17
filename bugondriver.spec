# norootforbuild

Name:           bugondriver
Version:                1.0
Release:                0
Summary:                BUGON Kernel Module Package
License:                GPL
Group:          System/Kernel
Source0:                %{name}-%{version}.tar.bz2
BuildRequires:  %kernel_module_package_buildreqs
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

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
       # Required to sign modules:  Invoke kernel-sign-file to sign each module
       for x in $(find $INSTALL_MOD_PATH/lib/modules/*-$flavor/ -name '*.ko'); do
               /usr/lib/rpm/pesign/kernel-sign-file -i pkcs7 sha256 $PWD/obj/$flavor/signing_key.priv $PWD/obj/$flavor/signing_key.x509 $x
       done
done

%changelog
