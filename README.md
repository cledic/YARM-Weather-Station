# YARM-Weather-Station
Very simple application using YARM modules and Acqua board [See here] (https://www.youtube.com/watch?v=HbdsCkS3KM4)

I use two YARM module and an Acqua LCD board for this very simple application.

A remote YARM module, connected to a BME280 chip, send the temperature, humidity and pressure value.

Another YARM module is attached to the Acqua board using a seria connection. This local module send the values received using a simple JSON structure.

On the Acqua board are running a couple of python script. I sue 64MB of ram disk to store temporary files.

First, run the "**download_info.sh**" script. This script run the "**mk_ramdisk.sh**" and "**sync_time.sh**" scripts, and then run a forever loop, paused for _600 sec_. Inside this loop I run two python script: "**ansa_reader.py**" and "**weather_reader.py**".

The "**ansa_reader.py**" script read the RSS from the Italian ANSA web site. Then save _title_ and _text_ of each news on the ramdisk as separated file.

The "**weather_reader.py**" script is a python library to download weather info from the [World Weather OnLine](www.worldweatheronline.com) You need a "**key**" to access the web API. This script download weather and icons and save, as separate files on ramdisk, all the information.

Then you need to run the "**serial_tst.py**" script. This script read from the serial interface the JSON string received and save a file. It print out the received JSON string.

Last but not least you need to run the "**YARM_Station.py**" script. This script use python game to access the Acqua frame buffer and to make string and icons look better! [See here] (https://www.youtube.com/watch?v=HbdsCkS3KM4) for the result!




