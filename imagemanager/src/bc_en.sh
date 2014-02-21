#!/bin/sh 
LABEL=$1
DIR_FROM=$2
DIRECTORY=/hdd
DATE=`date +%Y%m%d`
MKFS=/sbin/mkfs.jffs2
BACKUPIMAGE="e2jffs2.img"
BACKUPTAR="$1.tar"
BACKUPTARGZ="$1.tar.gz" 
ISAVAILABLE=`mount | grep hdd`
if [ -z "$ISAVAILABLE" ]; then
	echo "Try to mount sda1 to /media/hdd"
	mount /dev/sda1 /media/hdd
	ISAVAILABLE=`mount | grep sda1`
fi

if [ ! -z "$ISAVAILABLE" ]; then
	if grep -qs 'spark' /proc/stb/info/model ; then
		BOXTYPE=SPARK
		OPTIONS="-e 0x20000 -n"
	else
		echo "Box not found !!!"
		exit 0
	fi

	echo $BOXTYPE " found"
  echo ""
	if [ ! -f $MKFS ] ; then
		echo $MKFS" not found"
		exit 0
	fi

	rm -rf "$DIRECTORY/tmp/root"
	mkdir -p "$DIRECTORY/tmp/root"
	if [ ! -e "$DIRECTORY/enigma2-$DATE-$LABEL-$3" ]; then
		mkdir -p "$DIRECTORY/enigma2-$DATE-$LABEL-$3"
	fi

  if  [[ "$LABEL" = "NAND" ]] ; then
    mount -t jffs2 /dev/mtdblock6 "$DIRECTORY/tmp/root"
  else
    mount "$DIR_FROM" "$DIRECTORY/tmp/root"
  fi
  echo "Partition $LABEL mounted"
  echo ""                               
     
  if [ ! -f "$DIRECTORY/tmp/root/boot/uImage" ] ; then
		echo "no uImage!"
    echo "to create a valid archive"
    echo "copy uImage in the folder /boot"
    cd /root
    umount "$DIRECTORY/tmp/root"
		exit 0
	fi
  
  if [[ "$4" = "YES" ]]; then
    mv "$DIRECTORY/tmp/root/etc/enigma2/settings" "$DIRECTORY/tmp"
  fi
  
  if [[ "$3" = "IMG" ]]; then
    BACKUP=$BACKUPIMAGE
    echo " Please wait, copying uImage"
    echo ""
    cp "$DIRECTORY/tmp/root/boot/uImage" "$DIRECTORY/enigma2-$DATE-$LABEL-$3/uImage" 
    echo "Please wait, $BACKUP is created" 
    $MKFS --root="$DIRECTORY/tmp/root" --faketime --output="$DIRECTORY/tmp/$BACKUP" $OPTIONS
  elif [[ "$3" = "TAR" -o "$3" = "TARGZ" ]]; then
    BACKUP=$BACKUPTAR 
    echo "Please wait, $BACKUPTAR is created"
    cd "$DIRECTORY/tmp/root"
    tar -cf "$DIRECTORY/tmp/$BACKUP" *    
    if [[ "$3" = "TARGZ" ]]; then
    echo "Please wait, $BACKUPTARGZ is created"
    cd "$DIRECTORY/tmp"
    gzip "$BACKUP"
    BACKUP=$BACKUPTARGZ 
    fi
  fi    
    
  if [[ "$4" = "YES" ]]; then
    mv "$DIRECTORY/tmp/settings" "$DIRECTORY/tmp/root/etc/enigma2"
  fi     
  
    echo ""
    echo "Please wait, copying $BACKUP"
    echo ""
    mv  "$DIRECTORY/tmp/$BACKUP" "$DIRECTORY/enigma2-$DATE-$LABEL-$3/"
  if [ -f "$DIRECTORY/enigma2-$DATE-$LABEL-$3/$BACKUP" ] ; then
    echo "***********************************************************************"
    echo "Your $BACKUP can be found in:  $DIRECTORY/enigma2-$DATE-$LABEL-$3"
    echo "***********************************************************************"
    else
    echo "******************"
    echo "  Sorry, Error"
    echo "******************"
  fi
  cd /root
  sync
  umount "$DIRECTORY/tmp/root"
  echo "Partition $LABEL unmounted "
  echo ""
  rm -rf "$DIRECTORY/tmp"
  else
  echo "No hdd or usb-stick found!"
  exit 0
fi
exit