#!/bin/sh

#DIRECTORY=$1
DIRECTORY="/media/hdd"
MTDBOOT=5
MTDROOT=6
ISAVAILABLE=`mount | grep hdd`
if [ -z "$ISAVAILABLE" ]; then
	echo "Try to mount sda1 to /media/hdd"
	mount /dev/sda1 /media/hdd
	ISAVAILABLE=`mount | grep sda1`
fi

if [ ! -z "$ISAVAILABLE" ]; then
	if grep -qs 'spark' /proc/stb/info/model ; then
		BOXTYPE=spark
		OPTIONS="-e 0x20000 -n"
	else
		echo "Box not found !!!"
		exit 0
	fi


	echo $BOXTYPE " found"

	DATE=`date +%Y%m%d`
	MKFS=/sbin/mkfs.jffs2
	BACKUPIMAGE="e2jffs2.img"

	if [ ! -f $MKFS ] ; then
		echo $MKFS" not found"
		exit 0
	fi

	rm -rf "$DIRECTORY/tmp/root"
	mkdir -p "$DIRECTORY/tmp/root"
	if [ ! -e "$DIRECTORY/enigma2-$DATE" ]; then
		mkdir -p "$DIRECTORY/enigma2-$DATE"
	fi

	mount -t jffs2 /dev/mtdblock$MTDROOT "$DIRECTORY/tmp/root"

	echo "Copying uImage"
	cp /boot/uImage "$DIRECTORY/enigma2-$DATE/uImage"

	echo "Create root.jffs2, please wait..."
	$MKFS --root="$DIRECTORY/tmp/root" --faketime --output="$DIRECTORY/tmp/$BACKUPIMAGE" $OPTIONS

	mv "$DIRECTORY/tmp/$BACKUPIMAGE" "$DIRECTORY/enigma2-$DATE/"
	if [ -f "$DIRECTORY/enigma2-$DATE/$BACKUPIMAGE" ] ; then
		echo "$BACKUPIMAGE can be found in: $DIRECTORY/enigma2-$DATE"
	else
		echo "Error"
	fi
	sync
	umount "$DIRECTORY/tmp/root"
	rm -rf "$DIRECTORY/tmp/root"
else
	echo "No hdd or usb-stick found!"
	exit 0
fi
exit 0
