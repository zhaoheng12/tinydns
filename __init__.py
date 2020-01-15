# -*- coding: utf-8 -*-
with open("tinydns.conf","r") as f:
	info = f.read()

dict_info = eval(info)
print (dict_info)