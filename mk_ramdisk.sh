#!/bin/sh

echo -n "Mounting RAMDisk... "

grep /tmp/images /etc/mtab > /dev/null
if [ $? -eq 0 ]; then
  echo "already mounted..."
  exit
fi

if [ ! -e /tmp/images ]; then
  mkdir /tmp/images
fi

#
mount -t tmpfs -o size=64M,mode=0744 tmpfs /tmp/images/
chmod 777 /tmp/images/ -R

echo "done!"



