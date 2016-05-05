#!/bin/bash

ssh -Y blc00 "source /home/davidm/pulsar_software/pulsar.bash; python quicklook.py latest" #& \
ssh -Y blc01 "source /home/davidm/pulsar_software/pulsar.bash; python quicklook.py latest" #& \
ssh -Y blc02 "source /home/davidm/pulsar_software/pulsar.bash; python quicklook.py latest" #& \
ssh -Y blc03 "source /home/davidm/pulsar_software/pulsar.bash; python quicklook.py latest" #& \
ssh -Y blc04 "source /home/davidm/pulsar_software/pulsar.bash; python quicklook.py latest" #& \
ssh -Y blc05 "source /home/davidm/pulsar_software/pulsar.bash; python quicklook.py latest" #& \
ssh -Y blc06 "source /home/davidm/pulsar_software/pulsar.bash; python quicklook.py latest" #& \
ssh -Y blc07 "source /home/davidm/pulsar_software/pulsar.bash; python quicklook.py latest"
