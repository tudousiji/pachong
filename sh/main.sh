#!/bin/bash
source $HOME/.bashrc
source /etc/profile
source ~/.bash_profile
#phantomjs >> /home/python/phantomjs.log 2>&1
cd /home/python/
/root/anaconda3/bin/python /home/python/main.py >> /home/python/main.log 2>&1
