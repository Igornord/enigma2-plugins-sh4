#!/bin/sh
LOG(){
echo "$1"
echo "$1" >>/tmp/dba.log
echo "$1" >/hdd/DuckBA.log
}

GOTERROR(){
echo "$1"
echo "$1" >>/tmp/dba.log
echo "$1" >/hdd/DuckBA.log
touch /tmp/dba.error
exit 1
}

echo "##### setIMG.sh `date` #####" >/hdd/DuckBA.log
DBApath="/usr/lib/enigma2/python/Plugins/Extensions/DuckBA"

[ -f /tmp/dba.ok ] && rm -rf /tmp/dba.ok
[ -f /tmp/dba.error ] && rm -rf /tmp/dba.error
[ -f /tmp/dba.log ] && rm -rf /tmp/dba.log

#checking parameters
if [ -z $1 ]; then
	GOTERROR "usage: setIMG.sh [NAND|USB sd[abcd][1-9]]"
else
    if  [ -z $2 ]; then
	if ! [ $1 == "NAND" ]; then
	    GOTERROR "For boot from USB use: setIMG.sh USB sd[abcd][1-9]"
	fi
    fi
fi

sdXY=`echo $2 | sed "s;/dev/;;"`
echo "Active partition: '$sdXY'"

# do we realy need to change anything?
if `cat /proc/cmdline | grep -q "/dev/$sdXY"`; then
	if `echo $1 | grep -q 'USB'`; then
	    LOG "estart current soft from $sdXY"
	    touch /tmp/dba.ok
	    sync
	    exit 0
	fi
fi
if `cat /proc/cmdline | grep -q '/dev/mtdblock6'`; then
	if `echo $1 | grep -q 'NAND'`; then
	    LOG "Restart current soft from NAND"
	    touch /tmp/dba.ok
	    sync
	    exit 0
	fi
fi

#######################################
########## checking box type ##########
#######################################
if `cat /proc/stb/info/model | grep -q spark7162`; then
	LOG "spark7162 detected :)"
	MyBootCMD="nboot.i 0x80000000 0  0x18000000 ;bootm 0x80000000"
	MyBootARGS=""
	MyDuckBA_bootcmd='nboot.i 80000000 0 18400000;run DuckBA_bootargs;bootm 80000000;set bootargs ${bootargs_enigma2};nboot.i 80000000 0 18000000;bootm 80000000'
	MyDuckBA_bootargs='setenv bootargs "console=ttyAS0,115200 rw root=/dev/'$sdXY' init=/bin/devinit coprocessor_mem=4m@0x40000000,4m@0x40400000 printk=1 nwhwconf=device:eth0,hwaddr:00:80:E1:12:40:61 ip=172.100.100.249:172.100.100.174:172.100.100.174:${netmask}:Enigma2:eth0:off stmmaceth=msglvl:0,phyaddr:2,watchdog:5000 bigphysarea=6000 rootdelay=9"'
	[ -e /tmp/fw_env.config ] || ln -sf $DBApath/bin/fw_env.config.spark7162 /tmp/fw_env.config
elif `cat /proc/stb/info/model | grep -q spark`; then
	LOG "spark detected :)"
	MyBootCMD="nboot.i 80000000 0 18000000;bootm 80000000"
	MyBootARGS=""
	MyDuckBA_bootcmd='nboot.i 80000000 0 18400000;run DuckBA_bootargs;bootm 80000000;set bootargs ${bootargs_enigma2};nboot.i 80000000 0 18000000;bootm 80000000;reset'
	MyDuckBA_bootargs='setenv bootargs "console=ttyAS0,115200 root=/dev/'$sdXY' rw init=/bin/devinit coprocessor_mem=4m@0x40000000,4m@0x40400000 printk=1 nwhwconf=device:eth0,hwaddr:${ethaddr} rw ip=${ipaddr}:${serverip}:${gatewayip}:${netmask}:SPARK:eth0:off bigphysarea=6000 stmmaceth=msglvl:0,phyaddr:2,watchdog:5000 rootdelay=9"'
	[ -e /tmp/fw_env.config ] || ln -sf $DBApath/bin/fw_env.config.spark /tmp/fw_env.config
else
	GOTERROR "unknown box detected :("
	exit 1
fi

SCIEZKA="$DBApath/bin"

if `echo $1 | grep -q 'USB'`; then
	if ! `echo $2 | grep -q 'sd[abcd][1-9]'`; then
		GOTERROR "Error, got incorrect parametr :( ($1)"
		exit 1
	fi
	DuckBA_bootargs=$MyDuckBA_bootargs
	DuckBA_bootcmd=$MyDuckBA_bootcmd
	#MAIN_bootcmd='nboot.i 80000000 0 18000000;bootm 80000000'
	########################################
	########## mounting partition ##########
	########################################

	#unmouting partition if already mounted
	if `mount | grep '/tmp/DBA' | grep -q /dev/$sdXY`; then
		LOG "unmounting /tmp/DBA folder"
		umount /tmp/DBA 2>/dev/null
		umount /tmp/DBA 2>/dev/null
	fi
	if `mount | grep '/tmp/DBA' | grep -q /dev/$sdXY`; then
		GOTERROR "ERROR, partition cannot be unmounted :("
		exit 1
	fi

	#jesli brakuje naszego katalogu, musimy go zalozyc
	if [ ! -d /tmp/DBA ]; then
		LOG "Creating /tmp/DBA folder"
		mkdir /tmp/DBA
	fi
	#jesli nasza partycja jest niezamontowana, sprawdzmy jej konsystencje
	if ! `mount | grep -q /dev/$sdXY`; then
		LOG "checking partition consistency"
		e2fsck -p /dev/$sdXY
	fi

	#montowanie odpowiedniej partycji
	LOG "mounting partition"
	mount /dev/$sdXY /tmp/DBA
	if ! `mount | grep -q /dev/$sdXY`; then
		GOTERROR "BLAD montowania partycji, koncze prace"
		exit 1
	fi
	if [ ! -e /tmp/DBA/boot/uImage ]; then
		GOTERROR "BLAD: Zamontowana partycja nie zawiera pliku /boot/uImage. Koncze prace!!!"
		exit 1
	fi
	#some improvements
	sed -i "s/\$1\$K\$Oy86o0YspthTr2IXvUm751//" /tmp/DBA/etc/passwd
	############################################
	########## programming 2nd kernel ##########
	############################################

	LOG "Erasing 2nd kernel space in flash..."
	echo "ErASE nAnd.." >/dev/vfd
	$SCIEZKA/flash_erase /dev/mtd5 0x400000 0x20
	[ $? -gt 0 ] && GOTERROR "error erasing nand"

	LOG "Writing 2nd kernel to NAND..."
	echo "FLASH nAnd.." >/dev/vfd
	$SCIEZKA/nandwrite --start=0x400000 --pad /dev/mtd5 /tmp/DBA/boot/uImage
	[ $? -gt 0 ] && GOTERROR "error writing nand"
else #################################### boot from NAND ###################################################
	DuckBA_bootargs=$MyBootARGS
	DuckBA_bootcmd=$MyBootCMD
fi

##########################################
########## checking environment ##########
##########################################

if `cat /proc/stb/info/model | grep -q spark7162`; then
	if `cat /proc/mtd | grep -q 'mtd7: 00100000 00010000 "uboot"'`; then
		LOG "spark7162, i2s.ko module already loaded"
	else
		LOG "spark7162, we need to insmod i2s.ko module"
		insmod /lib/modules/i2s.ko
		[ $? -gt 0 ] && GOTERROR "error inserting i2s module"
	fi
fi

[ -e $SCIEZKA/fw_printenv ] || ln -sf $SCIEZKA/fw_setenv $SCIEZKA/fw_printenv
myENV=`$SCIEZKA/fw_printenv`
RET=$?
if [ $RET -eq 0 ]; then
	LOG "Valid fw_env detected :)"
else
	GOTERROR "fw_env misconfigured :("
fi

#activating DBA
LOG "Writing bootargs..."
#DuckBA_bootargs
$SCIEZKA/fw_setenv DuckBA_bootargs "$DuckBA_bootargs"
[ $? -gt 0 ] && GOTERROR "error writing DuckBA_bootargs"

#DuckBA_bootcmd
$SCIEZKA/fw_setenv bootcmd "$DuckBA_bootcmd"
[ $? -gt 0 ] && GOTERROR "error writing DuckBA_bootcmd"

#To check if all required written correctly
myENV=`$SCIEZKA/fw_printenv`
if ! `echo $myENV | grep -q "bootcmd="`;then
	[ $? -gt 0 ] && GOTERROR "error no bootcmd found after flashing"
fi
if ! `echo $myENV | grep -q "bootargs="`;then
	$SCIEZKA/fw_setenv DuckBA_ON
	[ $? -gt 0 ] && GOTERROR "error no bootargs found after flashing"
fi

########## cleaning trashes ##########
LOG "cleaning up..."
if `echo $myENV | grep -q "DuckBA_ON"`;then
	$SCIEZKA/fw_setenv DuckBA_ON
	[ $? -gt 0 ] && GOTERROR "error removing DuckBA_ON"
fi
if `echo $myENV | grep -q "DuckBA_sda_NO"`;then
	$SCIEZKA/fw_setenv DuckBA_sda_NO
	[ $? -gt 0 ] && GOTERROR "error removing DuckBA_sda_NO"
fi

if `echo $myENV | grep -q "DuckBA_bootcmd"`;then
	$SCIEZKA/fw_setenv DuckBA_bootcmd
	[ $? -gt 0 ] && GOTERROR "error removing DuckBA_bootcmd"
fi

if `echo $myENV | egrep -q "bootargsusb|menu_|bootcmdusb|bootargshub|bootcmdhub|bootargside|bootcmdide"`; then
	for i in `cat /proc/partitions | grep sd[abcd]. | awk '{print $4}' | sed 's/sd.//'`
	do
		$SCIEZKA/fw_setenv "menu_$i"
		[ $? -gt 0 ] && GOTERROR "error removing menu_$i"
		$SCIEZKA/fw_setenv "bootargsusb$i"
		[ $? -gt 0 ] && GOTERROR "error removing  bootargsusb$i"
		$SCIEZKA/fw_setenv "bootcmdusb$i"
		[ $? -gt 0 ] && GOTERROR "error removing bootcmdusb$i"
		$SCIEZKA/fw_setenv "bootargshub$i"
		[ $? -gt 0 ] && GOTERROR "error removing bootargshub$i"
		$SCIEZKA/fw_setenv "bootcmdhub$i"
		[ $? -gt 0 ] && GOTERROR "error removing bootcmdhub$i"
		$SCIEZKA/fw_setenv "bootargside$i"
		[ $? -gt 0 ] && GOTERROR "error removing bootargside$i"
		$SCIEZKA/fw_setenv "bootcmdide$i"
		[ $? -gt 0 ] && GOTERROR "error removing bootcmdide$i"
	done
fi

# some cleanings
if `cat /proc/stb/info/model | grep -q spark7162`; then
	if `cat /proc/mtd | grep -q 'mtd7: 00100000 00010000 "uboot"'`; then
		LOG "spark7162, we need to rmmod i2s.ko module after flashing"
		rmmod i2s.ko
		#[ $? -gt 0 ] && GOTERROR "error unloading i2s module"
	fi
fi

#writing DuckBA plugin if doesn't exists or if it is outdated
if `mount | grep -q '/tmp/DBA'`; then
	if [ ! -e "/tmp/DBA/usr/lib/enigma2/python/Plugins/Extensions/DuckBA" ]; then
		LOG "Writing DuckBA to newly activated fresh image..."
		cp -rf /usr/lib/enigma2/python/Plugins/Extensions/DuckBA /tmp/DBA/usr/lib/enigma2/python/Plugins/Extensions/DuckBA
	elif [ ! -f "/tmp/DBA/usr/lib/enigma2/python/Plugins/Extensions/DuckBA/VERSION" ]; then
		LOG "Updating DuckBA in newly activated image..."
		cp -rf /usr/lib/enigma2/python/Plugins/Extensions/DuckBA /tmp/DBA/usr/lib/enigma2/python/Plugins/Extensions/DuckBA
	else
		currenVERSION=`cat /usr/lib/enigma2/python/Plugins/Extensions/DuckBA/VERSION`
		dbaVERSION=`cat /tmp/DBA/usr/lib/enigma2/python/Plugins/Extensions/DuckBA/VERSION`
		if [ $currenVERSION -gt $dbaVERSION ]; then
			LOG "Updating DuckBA to newest version in newly activated image..."
			cp -rf /usr/lib/enigma2/python/Plugins/Extensions/DuckBA /tmp/DBA/usr/lib/enigma2/python/Plugins/Extensions/DuckBA
		else
			LOG "Updating of DuckBA not needed :)"
		fi
	fi
	umount /tmp/DBA
fi
touch /tmp/dba.ok
sync
