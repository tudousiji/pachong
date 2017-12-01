1.source $HOME/.bashrc 中添加环境变量 export PATH="/root/phantomjs-2.1.1-linux-x86_64/bin:$PATH"，也就是 phantomjs 的位置
2. sed -i "s/\r//" ./* 或者  cat -A fileName  把win文件转linux 文件
3.查看当前内存使用  cat /proc/meminfo
4.查看被杀进程  dmesg |grep python
5.查看当前进程内存使用 ps aux | grep python
6.linux 升级python方法: http://blog.csdn.net/u014749862/article/details/54429756
7.下载phantomjs http://phantomjs.org/download.html
8.pip install selenium
9.pip install pyexcel_xls