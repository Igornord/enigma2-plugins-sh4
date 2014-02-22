insmod /lib/modules/i2s.ko
fw_setenv bootdelay 3
fw_setenv baudrate 115200
fw_setenv yw_version YW_1.1.003-9-g7248322
fw_setenv board pdk7105
fw_setenv monitor_base 0
fw_setenv monitor_len 0x00100000
fw_setenv load_addr 0x80000000
fw_setenv HOSTNAME LINUX7167
fw_setenv ethaddr 00:80:E1:12:06:38
fw_setenv netmask 255.255.255.0
fw_setenv bootcmd_spark 'nboot.i 0x80000000 0  0x00100000 ;bootm 0x80000000'
fw_setenv bootcmd_enigma2 'nboot.i 0x80000000 0  0x18000000 ;bootm 0x80000000'
fw_setenv kernel_base_spark 0x00100000
fw_setenv kernel_base_enigma2 0x18000000
fw_setenv kernel_len_spark 0x00a00000
fw_setenv kernel_len_enigma2 0x00800000
fw_setenv erase_env 'mw.b $load_addr 0 0x20000;eeprom write $load_addr 0x000a0000 0x20000'
fw_setenv loadu_uboot 'fatload usb 0 $load_addr u-boot.bin'
fw_setenv loadu_kernel 'fatload usb 0 $load_addr $kernel_name'
fw_setenv loadu_kernel_spark 'fatload usb 0 $load_addr mImage'
fw_setenv loadu_kernel_enigma2 'fatload usb 0 $load_addr uImage'
fw_setenv loadu_userfs 'fatload usb 0 $load_addr $userfs_name'
fw_setenv loadu_userfs_spark 'fatload usb 0 $load_addr userfsub.img'
fw_setenv loadu_userfs_enigma2 'fatload usb 0 $load_addr e2jffs2.img'
fw_setenv tftp_uboot 'tftp $load_addr u-boot.bin'
fw_setenv tftp_kernel 'tftp $load_addr $tftp_kernel_name'
fw_setenv tftp_kernel_spark 'tftp $load_addr mImage'
fw_setenv tftp_kernel_enigma2 'tftp $load_addr uImage'
fw_setenv tftp_userfs 'tftp $load_addr $tftp_userfs_name'
fw_setenv tftp_userfs_spark 'tftp $load_addr userfsub.img'
fw_setenv tftp_userfs_enigma2 'tftp $load_addr e2jffs2.img'
fw_setenv erase_kernel 'nand erase  0x00100000  0x00a00000'
fw_setenv erase_userfs 'nand erase  0x01400000  0x16c00000'
fw_setenv erase_kernel_enigma2 'nand erase  0x18000000  0x00800000'
fw_setenv erase_userfs_enigma2 'nand erase  0x18800000  0x07700000'
fw_setenv write_kernel 'nand write.i 0x80000000 0x00100000 $filesize'
fw_setenv write_userfs 'nand write.yaffs2 0x80000000 0x01400000 $filesize'
fw_setenv write_kernel_enigma2 'nand write.i 0x80000000 0x18000000 $filesize'
fw_setenv write_userfs_enigma2 'nand write.jffs2 0x80000000 0x18800000 $filesize'
fw_setenv update 'eeprom write $load_addr $monitor_base $monitor_len'
fw_setenv update_kernel 'nand erase  0x00100000  0x00a00000 ;nand write.i 0x80000000 0x00100000 $filesize'
fw_setenv update_userfs 'nand erase  0x01400000  0x16c00000 ;nand write.yaffs2 0x80000000 0x01400000 $filesize'
fw_setenv update_kernel_enigma2 'nand erase  0x18000000  0x00800000 ;nand write.i 0x80000000 0x18000000 $filesize'
fw_setenv update_userfs_enigma2 'nand erase  0x18800000  0x07700000 ;nand write.jffs2 0x80000000 0x18800000 $filesize'
fw_setenv tftp_kernel_name_spark mImage
fw_setenv tftp_kernel_name_enigma2 uImage
fw_setenv tftp_userfs_name_spark userfsub.img
fw_setenv tftp_userfs_name_enigma2 e2jffs2.img
fw_setenv kernel_name_spark 'spark/mImage'
fw_setenv kernel_name_enigma2 'enigma2/uImage'
fw_setenv userfs_name_spark 'spark/userfsub.img'
fw_setenv userfs_name_enigma2 'enigma2/e2jffs2.img'
fw_setenv userfs_base_spark 0x01400000
fw_setenv userfs_base_enigma2 0x18800000
fw_setenv userfs_len_spark 0x16c00000
fw_setenv userfs_len_enigma2 0x07700000
fw_setenv uboot_name 'u-boot.bin'
fw_setenv ubootnfspath '192.168.40.19:/opt/target'
fw_setenv kernelnfspath '192.168.40.19:/opt/target'
fw_setenv rootfsnfspath '192.168.40.19:/opt/target'
fw_setenv bootfromnfs 'console=ttyAS0,115200 rw root=/dev/nfs nfsroot=192.168.40.19:/opt/target,nfsvers=2,rsize=4096,wsize=8192,tcp nwhwconf=device:eth0,hwaddr:00:80:E1:12:40:61 ip=192.168.40.61:192.168.40.19:192.168.3.1:255.255.0.0:LINUX7167:eth0:off stmmaceth=msglvl:0,phyaddr:1,watchdog:5000 bigphysarea=7000'
fw_setenv bootargs_flash 'console=ttyAS1,115200 rw ramdisk_size=6144 root=/dev/ram0 init=/linuxrc nwhwconf=device:eth0,hwaddr:00:80:E1:12:40:69 ip=192.168.0.69:192.168.3.119:192.168.3.1:255.255.0.0:Spark:eth0:off stmmaceth=msglvl:0,phyaddr:1,watchdog:5000 bigphysarea=7000'
fw_setenv bootargs_spark 'console=ttyAS1,115200 rw ramdisk_size=6144 root=/dev/ram0 init=/linuxrc nwhwconf=device:eth0,hwaddr:00:80:E1:12:40:69 ip=192.168.0.69:192.168.3.119:192.168.3.1:255.255.0.0:Spark:eth0:off stmmaceth=msglvl:0,phyaddr:1,watchdog:5000 bigphysarea=7000'
fw_setenv bootargs_enigma2 'console=ttyAS1,115200 rw root=/dev/mtdblock6 rootfstype=jffs2 init=/bin/devinit coprocessor_mem=4m@0x40000000,4m@0x40400000 printk=1 nwhwconf=device:eth0,hwaddr:00:80:E1:12:40:61 ip=172.100.100.249:172.100.100.174:172.100.100.174:255.255.0.0:Enigma2:eth0:off stmmaceth=msglvl:0,phyaddr:2,watchdog:5000 bigphysarea=6000'
fw_setenv ywenv_version 1
fw_setenv kernel_base 0x18000000
fw_setenv kernel_len  0x00800000
fw_setenv kernel_name 'enigma2/uImage'
fw_setenv userfs_name 'enigma2/e2jffs2.img'
fw_setenv tftp_kernel_name uImage
fw_setenv tftp_userfs_name 'e2jffs2.img'
fw_setenv userfs_len 0x07700000
fw_setenv userfs_base 0x18800000
fw_setenv boot_system enigma2
fw_setenv fw_setenv stdin serial
fw_setenv stdout serial
fw_setenv stderr serial
fw_setenv filesize 6060000
fw_setenv fuseburned true
fw_setenv bootargs 'console=ttyAS1,115200 rw root=/dev/mtdblock6 rootfstype=jffs2 init=/bin/devinit coprocessor_mem=4m@0x40000000,4m@0x40400000 printk=1 nwhwconf=device:eth0,hwaddr:00:80:E1:12:40:61 ip=172.100.100.249:172.100.100.174:172.100.100.174:${netmask}:Enigma2:eth0:off stmmaceth=msglvl:0,phyaddr:2,watchdog:5000 bigphysarea=6000'
fw_setenv bootcmd 'nboot.i 0x80000000 0  0x18000000 ;bootm 0x80000000'
rmmod i2s