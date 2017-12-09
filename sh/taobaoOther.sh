#!/bin/bash
source $HOME/.bashrc
source /etc/profile
source ~/.bash_profile
cd /home/python/haoquanvip/
/root/anaconda3/bin/python /home/python/haoquanvip/taobaoOtherTask.py >> /home/python/haoquanvip/cronTabLog/taobaoOtherTask.log 2>&1
