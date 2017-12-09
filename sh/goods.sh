#!/bin/bash
source $HOME/.bashrc
source /etc/profile
source ~/.bash_profile
cd /home/python/haoquanvip/
/root/anaconda3/bin/python /home/python/haoquanvip/goodsTask.py >> /home/python/haoquanvip/cronTabLog/goodsTask.log 2>&1
