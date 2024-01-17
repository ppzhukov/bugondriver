# bugondriver for SUSE Linux
BUG(), BUG_ON(), dump_stack(), panic() example

#### Forked from https://lkw.readthedocs.io/en/latest/doc/06_kernel_bug_reporting.html
#### Linux Kernel Workbook
#### https://github.com/rishiba/
#### Copyright 2016, Rishi Agrawal
#### ---
#### https://openbuildservice.org/help/manuals/obs-user-guide/cha.obs.scm_ci_workflow_integration
#### https://documentation.suse.com/sbp/server-linux/html/SBP-KMP-Manual-SLE12SP2/index.html
#### https://linuxkamarada.com/en/2019/03/19/integrating-the-open-build-service-with-github/
#### [https://www.suse.com/c/using-opensuse-build-service-create-and-distribute-kernel-module-packages/](https://www.suse.com/c/using-opensuse-build-service-create-and-distribute-kernel-module-packages/)


## description

Kernel has built-in functions/macros for BUGS
BUG(), BUG_ON(), dump_stack() and panic() can be used in your code to report error conditions.
For more details on these function read the chapter Debugging in the book Linux Kernel Development, 3rd Edition, Robert love.
This chapter will give you example with the proc interface on how to use the debugging facilities given in the kernel.

## Make and install modules
[https://www.suse.com/c/using-sles-and-the-sle-sdk-build-kernel-module-package-kmp/](https://www.suse.com/c/using-sles-and-the-sle-sdk-build-kernel-module-package-kmp/)
Install needs packages to your system using commands bellow:
```bash
export KERNEL_VERSION=$(uname -r) # get Kernel version and Flavor
zypper in -y make gcc build kernel-sources-$(KERNEL_VERSION)
```
create Makefile
```
MYPROC=bugondriver
ARCH=x86_64
FLAVOR=default

obj-m += $(MYPROC).o

export KROOT=/usr/src/linux-obj/$(ARCH)/$(FLAVOR)

allofit:  modules

modules: clean

        @$(MAKE) -C $(KROOT) M=$(PWD) modules

modules_install:
        @$(MAKE) -C $(KROOT) M=$(PWD) modules_install

kernel_clean:
        @$(MAKE) -C $(KROOT) M=$(PWD) clean

clean: kernel_clean
        rm -rf   Module.symvers modules.order

insert: modules
        sudo dmesg -c
        sudo insmod bugondriver.ko

remove: clean
        sudo rmmod bugondriver
```
run
```bash
make insert
```
## Running the code

To run the code you will have to write to the _proc_ entry. Based on the value written the system will behave differently.
You can see the output in the dmesg output.

- BUG_ON 1
- BUG 2
- DUMPSTACK 3
- PANIC 4