# -*- coding: utf-8 -*-
# import os
# aa = os.system("dig @127.0.0.1 zhplz.com")
# print (aa)
import sys, getopt

def main(argv):

   print '=============='
   inputfile = '666'
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-i", "--ifile"):
         inputfile = arg

   print '输入的文件为：',


if __name__ == "__main__":
   main(sys.argv[1:])


