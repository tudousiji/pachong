#!/bin/bash
source $HOME/.bashrc
source /etc/profile
source ~/.bash_profile
cd /home/python/
/root/anaconda3/bin/python /home/python/hotKeyWordsTask.py >> /home/python/cronTabLog/hotKeyWordsTask.log 2>&1
