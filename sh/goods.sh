#!/bin/bash
source $HOME/.bashrc
source /etc/profile
source ~/.bash_profile
cd /home/python/
/root/anaconda3/bin/python /home/python/goodsTask.py >> /home/python/cronTabLog/goodsTask.log 2>&1
