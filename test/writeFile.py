import time

f = open("/home/python/testCronTab.txt", 'a', encoding='utf-8')
localTime = time.localtime(time.time());
writeTime=time.strftime('%Y-%m-%d %H:%M:%S', localTime)
f.write("testCronTab:"+writeTime)
f.flush()
f.close()