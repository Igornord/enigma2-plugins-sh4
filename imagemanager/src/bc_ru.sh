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

	echo "Обнаружена платформа "$BOXTYPE
  echo ""
	if [ ! -f $MKFS ] ; then
		echo $MKFS" не найден!"
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
    echo "Раздел $LABEL примонтирован"
    echo "" 
    
  if [ ! -f "$DIRECTORY/tmp/root/boot/uImage" ] ; then
		echo "отсутствует uImage!"
    echo "для создания корректного архива"
    echo "положите uImage в папку /boot"
    cd /root
    umount "$DIRECTORY/tmp/root"
		exit 0
	fi                              
  
  if [[ "$4" = "YES" ]]; then
    mv "$DIRECTORY/tmp/root/etc/enigma2/settings" "$DIRECTORY/tmp"
  fi
  
  if [[ "$3" = "IMG" ]]; then
    BACKUP=$BACKUPIMAGE
    echo "Пожалуйста подождите, копируется uImage"
    echo ""
    cp "$DIRECTORY/tmp/root/boot/uImage" "$DIRECTORY/enigma2-$DATE-$LABEL-$3/uImage" 
    echo "Пожалуйста подождите, создается "$BACKUP 
    $MKFS --root="$DIRECTORY/tmp/root" --faketime --output="$DIRECTORY/tmp/$BACKUP" $OPTIONS
  elif [[ "$3" = "TAR" -o "$3" = "TARGZ" ]]; then
    BACKUP=$BACKUPTAR 
    echo "Пожалуйста подождите, создается "$BACKUPTAR
    cd "$DIRECTORY/tmp/root"
    tar -cf "$DIRECTORY/tmp/$BACKUP" *    
    if [[ "$3" = "TARGZ" ]]; then
    echo "Пожалуйста подождите, создается "$BACKUPTARGZ
    cd "$DIRECTORY/tmp"
    gzip "$BACKUP"
    BACKUP=$BACKUPTARGZ 
    fi
  fi    
    
  if [[ "$4" = "YES" ]]; then
    mv "$DIRECTORY/tmp/settings" "$DIRECTORY/tmp/root/etc/enigma2"
  fi     
  
    echo ""
    echo "Пожалуйста подождите, копируется $BACKUP"
    echo ""
    mv  "$DIRECTORY/tmp/$BACKUP" "$DIRECTORY/enigma2-$DATE-$LABEL-$3/"
  if [ -f "$DIRECTORY/enigma2-$DATE-$LABEL-$3/$BACKUP" ] ; then
    echo "***********************************************************************"
    echo "Ваш архив $BACKUP находится в: $DIRECTORY/enigma2-$DATE-$LABEL-$3"
    echo "***********************************************************************"
    else
    echo "******************************"
    echo "  Увы, произошла ошибка!  "
    echo "******************************"
  fi
  cd /root
  sync
  umount "$DIRECTORY/tmp/root"
  echo "Раздел $LABEL отмонтирован."
  echo ""
  rm -rf "$DIRECTORY/tmp"
  else
  echo "USB-Флешка не обнаружена!"
  exit 0
fi
exit
