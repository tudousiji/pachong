#!/bin/bash
source $HOME/.bashrc
source /etc/profile
source ~/.bash_profile
#phantomjs >> /home/python/phantomjs.log 2>&1
cd /home/python/haoquanvip/
/root/anaconda3/bin/python /home/python/haoquanvip/main.py >> /home/python/haoquanvip/cronTabLog/main.log 2>&1
