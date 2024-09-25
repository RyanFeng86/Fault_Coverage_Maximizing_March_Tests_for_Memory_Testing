# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 23:22:38 2020

@author: boxuanl
"""

from march_test import March_test

memory = []
for i in range(4):
    memory.append("")
#print("Initial Memory : ",memory)
i_m=memory.copy()

import csv
csv_file=csv.reader(open(r'fault_list_all.csv','r'))
fault_list = []
for line in csv_file:
    fault_list.append(line[0:10])
    
hangshu = 1
#fault_list = ['CFdrd', '0_0', '0', '0', 'NA', '1', '0', 'r0', '1', '0'], ['CFdrd', '0_0', '0', '0', 'NA', '2', '0', 'r0', '1', '0']
print(fault_list)
filereader = open('best6.txt', 'r')
f=filereader.readlines()

for (line_num,line) in enumerate(f):
    fenzi     = 0
    fenmu     = 0
    current_type = ''
    current_subtype = ''
    count = 1
    f_count = 0
    f_count_p = 0
    for fault in fault_list:
        fault[2] = int(fault[2])
        fault[5] = int(fault[5])
        #print("fault is now", fault)
        memory = i_m.copy()
        march_line = line.strip().split(",")
        if ((fault[0] != current_type) or (fault[1] != current_subtype)):
            if (current_type != ''):
                print("============fault coverage for subtype", current_type, current_subtype, "is", f_count, "/", count, "============")
                fenzi = fenzi + f_count
                fenmu = fenmu + count
            count = 1
            f_count = 0
            f_count_p = 0
            current_type = fault[0]
            current_subtype = fault[1]
        else:
            count = count + 1
        print("------------------ fault introduced: ", fault[0], fault[1], "------------------")
        for march_element in march_line:
            print("march element is : ", march_element)
            f_count = March_test(march_element,memory,fault,line_num, f_count)
            if(f_count != f_count_p):
                f_count_p = f_count_p + 1
                break
            print("memory is now: ", memory)
        if (fault == fault_list[-1]):       #print fault coverage for last fault in the list 
            print("============fault coverage for subtype", current_type, current_subtype, "is", f_count, "/", count, "============")
            fenzi = fenzi + f_count
            fenmu = fenmu + count
            
    if (0 <= fenzi * 100 / fenmu):
        FC = fenzi * 100 / fenmu
        print(fenzi,"/",fenmu)
        print(hangshu, ",", FC)
        
    hangshu = hangshu + 1
            

    
        


