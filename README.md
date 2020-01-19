# tinydns
依赖的包
gevent,dnslib
python2 安装ConfigParser python3 安装configparser
基于gevent的dns服务
配置文件 /etc/tinydns.conf 可以自定义一些配置信息
服务运行命令：sudo tinydns -c  /etc/tinydns.conf
测试： dig @127.0.0.1 google.com
