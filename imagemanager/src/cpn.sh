#!/bin/sh
LABEL=$1
PART=$2
DIRECTORY=/hdd 

umount -l "$PART" > /dev/null
       
/sbin/tune2fs -L COPY_NAND $2 > /dev/null

rm -rf $DIRECTORY/tmp/root
mkdir -p $DIRECTORY/tmp/root

rm -rf $DIRECTORY/tmp/copy
mkdir -p $DIRECTORY/tmp/copy

mount -t jffs2 /dev/mtdblock6 $DIRECTORY/tmp/root
echo "Partition NAND-flash mounted"
echo ""       
mount $PART $DIRECTORY/tmp/copy  
echo "Partition $PART mounted"
echo "" 
 
rm -rf $DIRECTORY/tmp/copy/*   

if [[ "$3" = "YES" ]]; then
  mv $DIRECTORY/tmp/root/etc/enigma2/settings $DIRECTORY/tmp
  echo "Settings file is deleted"
  echo "" 
fi    
                           
echo "Please wait," 
echo "goes up the partition NAND-flash "
echo "to the specified section of the stick"
    
(cd $DIRECTORY/tmp/root && tar cf - .) | (cd $DIRECTORY/tmp/copy && tar xf -)     

if [[ "$3" = "YES" ]]; then
  mv $DIRECTORY/tmp/settings $DIRECTORY/tmp/root/etc/enigma2
fi 

cd /root 
sync
sleep 5
umount "$PART"
echo "Partition NAND-flash unmounted"
echo ""
umount $DIRECTORY/tmp/root 
echo "Partition $PART unmounted"
echo ""
rm -rf $DIRECTORY/tmp  
exit
