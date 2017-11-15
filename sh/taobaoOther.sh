#!/bin/bash
source $HOME/.bashrc
source /etc/profile
source ~/.bash_profile
cd /home/python/
/root/anaconda3/bin/python /home/python/taobaoOtherTask.py >> /home/python/cronTabLog/taobaoOtherTask.log 2>&1
