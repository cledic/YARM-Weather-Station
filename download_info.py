#!/bin/bash

/root/utility/sync_time.sh
/root/utility/mk_ramdisk.sh

cd /root/YARM_Station

#python serial_tst.py &

while true;
do
    python ./ansa_reader.py
    python ./weather_reader.py
    sleep 600
done

