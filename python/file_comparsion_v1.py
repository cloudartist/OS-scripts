#!/usr/bin/env python3

__author__ = 'marcin.taracha'

import sys
import argparse
import re
import subprocess

#Args setup section
parser = argparse.ArgumentParser(description='Script designed to compare two config files')
parser.add_argument('-i','--input', help='Two input files name -i <file1> <file2>',required=True,nargs='+')
args = parser.parse_args()

#Variables initalization
i = 0
sensitivity = 16
list_first = []
list_second = []
begining_of_file = ""
end_of_file = ["#####Exclusive for first document#######\n", "", "#####Exclusive for second document#######\n", ""]
#open file as string array
with open(args.input[0],'r') as new_file:
    for line in new_file.read().splitlines():
        list_first.append(line)
with open(args.input[1], 'r') as input_file:
    for line in input_file.read().splitlines():
        list_second.append(line)

with open(args.input[0], 'r') as new_file:
    main_text = new_file.read()
with open(args.input[1], 'r') as input_file:
    changed_text = input_file.read()

for item in list_first:
    if not re.search(item[:sensitivity],changed_text):
        b = 1
        end_of_file[1] += str(item+"\n")
    for lines in list_second:
        if re.search(item[:sensitivity], lines) and not re.search(lines,begining_of_file):
            begining_of_file += str(lines+"\n")
        elif not re.search(lines[:sensitivity],main_text) and not re.search(lines,end_of_file[3]):
            c = 1
            end_of_file[3] += str(lines+"\n")

with open("test.conf", "w") as myfile:
    myfile.write(begining_of_file)
    for diffrences in end_of_file:
        myfile.write(diffrences)
#Show bash diff between first input file and output
#subprocess.call(['diff -yt '+args.input[0]+' test.conf|head -n 10'], shell=True) 
