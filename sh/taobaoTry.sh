#!/bin/bash
source $HOME/.bashrc
source /etc/profile
source ~/.bash_profile
cd /home/python/
/root/anaconda3/bin/python /home/python/taobaoTryTask.py >> /home/python/cronTabLog/taobaoTryTask.log 2>&1
