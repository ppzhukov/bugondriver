# bugondriver for Linux (especialy SUSE)
BUG(), BUG_ON(), dump_stack(), panic() example

Supported OS: SLES15SP[345], OpenSUSE15.[345], CentOS[78], CentOS 8 Stream, Fedora3[789], Fedora Rawhide, ScientificLinux 7

![GPL3](https://img.shields.io/badge/license-GPLv3-blue)
[![build result](https://build.opensuse.org/projects/home:pzhukov:bugondriver/packages/bugondriver/badge.svg?type=percent)](https://build.opensuse.org/package/show/home:pzhukov:bugondriver/bugondriver)

[Repositories](https://software.opensuse.org//download.html?project=home%3Apzhukov%3Abugondriver&package=bugondriver)

> Forked from https://lkw.readthedocs.io/en/latest/doc/06_kernel_bug_reporting.html  
> Linux Kernel Workbook  
> https://github.com/rishiba/  

## description

Kernel has built-in functions/macros for BUGS
BUG(), BUG_ON(), dump_stack() and panic() can be used in your code to report error conditions.
For more details on these function read the chapter Debugging in the book Linux Kernel Development, 3rd Edition, Robert love.
This chapter will give you example with the proc interface on how to use the debugging facilities given in the kernel.

## Quick Start
* Add [Repositories](https://software.opensuse.org//download.html?project=home%3Apzhukov%3Abugondriver&package=bugondriver) to your system
* Install package
```bash
zypper in -y bugondriver-kmp-default
```
* load module
For an unupdated kernel:
```bash
insmod /lib/modules/$(uname -r)/extra/bugondriver.ko
```
For an updated kernel
```bash
insmod /lib/modules/$(uname -r)/weak-updates/extra/bugondriver.ko
```
* send signal to kernel
```bash
echo 4 > /proc/bugondriver
```

## Running the code

To run the code you will have to write to the _proc_ entry. Based on the value written the system will behave differently.
You can see the output in the dmesg output.

- BUG_ON 1
- BUG 2
- DUMPSTACK 3
- PANIC 4

example:
```bash
echo 2 > /proc/bugondriver
```

## Make and install modules manualy
### Set Up the Build System.
[https://www.suse.com/c/using-sles-and-the-sle-sdk-build-kernel-module-package-kmp/](https://www.suse.com/c/using-sles-and-the-sle-sdk-build-kernel-module-package-kmp/)
```bash
zypper in -t pattern Basis-Devel
zypper in build
```
### Make module. 
[https://docs.kernel.org/kbuild/modules.html](https://docs.kernel.org/kbuild/modules.html)
```bash
make -C /lib/modules/$(uname -r)/build M=$PWD
make -C /lib/modules/$(uname -r)/build M=$PWD modules_install
```
### Insert module.
```bash
insmod bugondriver.ko
```

## Appendix
### _service file for OBS
```xml
<services>
  <service mode="buildtime" name="set_version" />
  <service name="obs_scm">
    <param name="url">https://github.com/ppzhukov/bugondriver.git</param>
    <param name="scm">git</param>
    <param name="revision">main</param>
    <param name="extract">bugondriver.spec</param>
  </service>
  <service mode="buildtime" name="tar" />
  <service mode="buildtime" name="recompress">
    <param name="file">*.tar</param>
    <param name="compression">xz</param>
  </service>
</services>
```
#### [https://openbuildservice.org/help/manuals/obs-user-guide/cha.obs.scm_ci_workflow_integration](https://openbuildservice.org/help/manuals/obs-user-guide/cha.obs.scm_ci_workflow_integration)
#### [https://documentation.suse.com/sbp/server-linux/html/SBP-KMP-Manual-SLE12SP2/index.html](https://documentation.suse.com/sbp/server-linux/html/SBP-KMP-Manual-SLE12SP2/index.html)
#### [https://linuxkamarada.com/en/2019/03/19/integrating-the-open-build-service-with-github/](https://linuxkamarada.com/en/2019/03/19/integrating-the-open-build-service-with-github/)
#### [https://www.suse.com/c/using-opensuse-build-service-create-and-distribute-kernel-module-packages/](https://www.suse.com/c/using-opensuse-build-service-create-and-distribute-kernel-module-packages/)
