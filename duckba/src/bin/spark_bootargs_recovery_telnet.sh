fw_setenv baudrate 115200
fw_setenv board mb618
fw_setenv monitor_base 0xA0000000
fw_setenv monitor_len 0x00080000
fw_setenv monitor_sec "0xa0000000    0xa007ffff"
fw_setenv load_addr 0x80000000
fw_setenv unprot 'protect off $monitor_sec'
fw_setenv update 'protect off $monitor_sec;erase $monitor_sec;cp.b $load_addr $monitor_base $monitor_len;protect on $monitor_sec'
fw_setenv HOSTNAME LINUX7109
fw_setenv ethaddr "00:80:E1:12:06:38"
fw_setenv ipaddr "192.168.1.8"
fw_setenv netmask "255.255.255.0"
fw_setenv gatewayip "192.168.1.1"
fw_setenv serverip "192.168.1.3"
fw_setenv kernel_base_spark 0xa0080000
fw_setenv kernel_base_enigma2 0x18000000
fw_setenv kernel_sec 'a0080000 a077ffff'
fw_setenv kernel_len 0x00700000
fw_setenv update_kernel 'protect off  a0080000 a077ffff ;erase  a0080000 a077ffff ;cp.b 0x80000000 0xa0080000  0x00700000 ;protect on  a0080000 a077ffff'
fw_setenv rootfs_base 0xafff
fw_setenv menucmd update
fw_setenv tftp_kernel_name_spark mImage
fw_setenv tftp_kernel_name_enigma2 uImage
fw_setenv tftp_userfs_name_spark userfsub.img
fw_setenv tftp_userfs_name_enigma2 e2jffs2.img
fw_setenv kernel_name_spark "spark/mImage"
fw_setenv kernel_name_enigma2 "enigma2/uImage"
fw_setenv userfs_name_spark "spark/userfsub.img"
fw_setenv userfs_name_enigma2 "enigma2/e2jffs2.img"
fw_setenv userfs_base_spark 800000
fw_setenv userfs_base_enigma2 18800000
fw_setenv userfs_len_spark 17800000
fw_setenv userfs_len_enigma2 7700000
fw_setenv kernelnfspath "192.168.40.19:/opt/target"
fw_setenv rootfs_name UserFS
fw_setenv rootfsnfspath "192.168.40.19:/home/d22cj/workspace/target"
fw_setenv uboot_name u-boot.bin
fw_setenv ubootnfspath "192.168.40.19:/home/d22cj/workspace/target"
fw_setenv bootfromnfs 'nfs a4000000 $kernelnfspath/$kernel_name;bootm a4000000'
fw_setenv bootargs_nfs 'console=ttyAS0,115200 nwhwconf=device:eth0,hwaddr:00:80:E1:12:40:61 stmmaceth=msglvl:0,phyaddr:1:watchdog:5000 root=/dev/nfs nfsroot=192.168.40.19:/opt/target,nfsvers=2,rsize=4096,wsize=8192,tcp rw ip=192.168.40.61:192.168.40.19:192.168.3.1:255.255.0.0:LINUX7109:eth0:off bigphysarea=4000'
fw_setenv bootargs_flash 'console=ttyAS0,115200 rw ramdisk_size=6144 init=/linuxrc root=/dev/ram0 nwhwconf=device:eth0,hwaddr:00:80:E1:12:40:69 ip=192.168.0.69:192.168.3.119:192.168.3.1:255.255.0.0:lh:eth0:off stmmaceth=msglvl:0,phyaddr:1,watchdog:5000 bigphysarea=4000'
fw_setenv bootargs_spark 'console=ttyAS1,115200 rw ramdisk_size=6144 init=/linuxrc root=/dev/ram0 nwhwconf=device:eth0,hwaddr:00:80:E1:12:40:69 ip=192.168.0.69:192.168.3.119:192.168.3.1:255.255.0.0:lh:eth0:off stmmaceth=msglvl:0,phyaddr:1,watchdog:5000 bigphysarea=4000'
fw_setenv magic_version "1.7"
fw_setenv filesize 2BE6FFC
fw_setenv fuseburned true
fw_setenv bootdelay 2
fw_setenv bootargs_enigma2 'console=ttyAS0,115200 root=/dev/mtdblock6 rootfstype=jffs2 rw init=/bin/devinit coprocessor_mem=4m@0x40000000,4m@0x40400000 printk=1 nwhwconf=device:eth0,hwaddr:00:80:E1:12:40:69 rw ip=${ipaddr}:${serverip}:${gatewayip}:${netmask}:LINUX7109:eth0:off bigphysarea=6000 stmmaceth=msglvl:0,phyaddr:2,watchdog:5000'
fw_setenv bootargs 'console=ttyAS0,115200 root=/dev/mtdblock6 rootfstype=jffs2 rw init=/bin/devinit coprocessor_mem=4m@0x40000000,4m@0x40400000 printk=1 nwhwconf=device:eth0,hwaddr:00:80:E1:12:40:69 rw ip=${ipaddr}:${serverip}:${gatewayip}:${netmask}:LINUX7109:eth0:off bigphysarea=6000 stmmaceth=msglvl:0,phyaddr:2,watchdog:5000'
fw_setenv bootcmd 'nboot.i 80000000 0 18000000;bootm 80000000'
fw_setenv boot_system enigma2
fw_setenv userfs_base 18800000
fw_setenv userfs_len 7700000
fw_setenv kernel_base 0x18000000
fw_setenv kernel_name enigma2/uImage
fw_setenv userfs_name enigma2/e2jffs2.img
fw_setenv tftp_kernel_name uImage
fw_setenv tftp_userfs_name e2jffs2.img
fw_setenv stdin serial
fw_setenv stdout serial
fw_setenv stderr serial
