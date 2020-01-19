* tinydns

* 依赖的包 gevent,dnslib  python2:ConfigParser python3:configparser

* 方法1： pip install tinydns == 0.0.3

* 方法二： git clone https://github.com/zhaoheng12/tinydns.git

* 配置文件可以自定义一些配置信息 cd tinydns  cp tinydns.conf /etc/tinydns.conf

* 运行命令：sudo tinydns -c  /etc/tinydns.conf 或者 sudo tinydns -c tinydns.conf

* 测试： dig @127.0.0.1 google.com

