#!/bin/sh
LOG(){
echo "$1"
echo "$1" >>/tmp/dba.log
}

GOTERROR(){
echo "$1"
echo "$1" >>/tmp/dba.log
touch /tmp/dba.error
exit 1
} 

dbaPATH="/DuckBA/bin"
[ -f /tmp/dba.ok ] && rm -rf /tmp/dba.ok
[ -f /tmp/dba.error ] && rm -rf /tmp/dba.error
[ -f /tmp/dba.log ] && rm -rf /tmp/dba.log

if `cat /proc/stb/info/model | grep -q spark7162`; then
	LOG "spark7162 detected :)" 
	bootargs_spark=''
	insmod /lib/modules/i2s.ko
elif `cat /proc/stb/info/model | grep -q spark`; then
	bootargs_spark='console=ttyAS1,115200 rw ramdisk_size=6144 init=/linuxrc root=/dev/ram0 nwhwconf=device:eth0,hwaddr:00:80:E1:12:40:69 ip=192.168.0.69:192.168.3.119:192.168.3.1:255.255.0.0:lh:eth0:off stmmaceth=msglvl:0,phyaddr:1,watchdog:5000 bigphysarea=4000'
else
	[ $? -gt 0 ] && GOTERROR "Unknown box :("
	exit 1
fi

$dbaPATH/fw_setenv bootargs $bootargs_spark
[ $? -gt 0 ] && GOTERROR "error writing bootargs"
$dbaPATH/fw_setenv bootcmd "bootm  0xa0080000"
[ $? -gt 0 ] && GOTERROR "error writing bootcmd"
$dbaPATH/fw_setenv boot_system "spark"
[ $? -gt 0 ] && GOTERROR "error writing boot_system"
$dbaPATH/fw_setenv userfs_base "800000"
[ $? -gt 0 ] && GOTERROR "error writing userfs_base"
$dbaPATH/fw_setenv userfs_len "17800000"
[ $? -gt 0 ] && GOTERROR "error writing userfs_len"
$dbaPATH/fw_setenv kernel_base "0x00080000" 
[ $? -gt 0 ] && GOTERROR "error writing kernel_base"
$dbaPATH/fw_setenv kernel_name "spark/mImage"
[ $? -gt 0 ] && GOTERROR "error writing kernel_name"
$dbaPATH/fw_setenv userfs_name "spark/userfsub.img"
[ $? -gt 0 ] && GOTERROR "error writing userfs_name"
$dbaPATH/fw_setenv tftp_kernel_name "mImage"
[ $? -gt 0 ] && GOTERROR "error writing tftp_kernel_name"
$dbaPATH/fw_setenv tftp_userfs_name "userfsub.img" 
[ $? -gt 0 ] && GOTERROR "error writing tftp_userfs_name"
touch /tmp/dba.ok