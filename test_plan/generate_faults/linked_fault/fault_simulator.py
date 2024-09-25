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
csv_file=csv.reader(open(r'fault_list_LF2_av.csv','r'))
fault_list = []
temp = []
for line in csv_file:
    temp.append(line)
for i in range(1, len(temp), 2):
    fault_list.append([temp[i], temp[i+1]])

#fault_list = [[['TFs', '0', '0', '1', 'w0', '1', 'NA', 'NA', '0','0'], ['SAFs',	'0', '0', 'NA',	'w1', '0', 'NA', 'NA', '0', '0']]]
#fault_list = fault_list[0:5]

fault_report = open('fault_report.txt', 'w')  
fault_coverage = []
filereader = open('march_test.txt', 'r')
f=filereader.readlines()
for (line_num,line) in enumerate(f):
    current_type1 = ''
    current_subtype1 = ''
    current_type2 = ''
    current_subtype2 = ''
    count = 1
    f_count = 0
    f_count_p = 0
    for fault in fault_list:
        fault[0][2] = int(fault[0][2])
        fault[0][5] = int(fault[0][5])
        fault[1][2] = int(fault[1][2])
        fault[1][5] = int(fault[1][5])
        #print("fault is now", fault)
        memory = i_m.copy()
        march_line = line.strip().split(",")
        if ((fault[0][0] != current_type1) or (fault[0][1] != current_subtype1) or (fault[1][0] != current_type2) or (fault[1][1] != current_subtype2)):
            if (current_type1 != ''):
                #print("============fault coverage for subtype", current_type1, current_subtype1, " ", current_type2, current_subtype2, "is", f_count, "/", count, "============")
                fault_report.write(current_type1 + current_subtype1 + "," + current_type2 + current_subtype2 + "," + str(f_count) + "," + str(count) +"\n")
                fault_coverage.append([current_type1 + current_subtype1, current_type2 + current_subtype2, f_count, count])
            count = 1
            f_count = 0
            f_count_p = 0
            current_type1 = fault[0][0]
            current_subtype1 = fault[0][1]
            current_type2 = fault[1][0]
            current_subtype2 = fault[1][1]
        else:
            count = count + 1
        #print("------------------ fault introduced: ", fault[0][0], fault[0][1], " and ", fault[1][0], fault[1][1], "------------------")
        for march_element in march_line:
            #print("march element is : ", march_element)
            f_count = March_test(march_element,memory,fault,line_num, f_count)
            if(f_count != f_count_p):
                f_count_p = f_count_p + 1
                break
            #print("memory is now: ", memory)
        if (fault == fault_list[-1]):       #print fault coverage for last fault in the list 
            #print("============fault coverage for subtype", current_type1, current_subtype1, " ", current_type2, current_subtype2, "is", f_count, "/", count, "============")
            fault_report.write(current_type1 + current_subtype1 + "," + current_type2 + current_subtype2 + "," + str(f_count) + "," + str(count) +"\n")
            fault_coverage.append([current_type1 + current_subtype1, current_type2 + current_subtype2, f_count, count])
fault_report.close()
#print (fault_coverage)

with open('LF2_av.csv', 'w', newline='') as cover_table:
    csv_write = csv.writer(cover_table)
    coupling_fault = ["CFinUP","CFinDOWN","CFidUP0","CFidUP1","CFidDOWN0","CFidDOWN1","CFst0_0", "CFst1_0", "CFst0_1","CFst1_1","CFds0r0_0","CFds1r1_0","CFds0r0_1","CFds1r1_1","CFds0w0_0","CFds0w1_0","CFds1w0_0","CFds1w1_0","CFds0w0_1","CFds0w1_1","CFds1w0_1","CFds1w1_1","CFtr0_0","CFtr1_0","CFtr0_1","CFtr1_1","CFwd0_0","CFwd1_0","CFwd0_1","CFwd1_1","CFrd0_0","CFrd1_0","CFrd0_1","CFrd1_1","CFdrd0_0","CFdrd1_0","CFdrd0_1","CFdrd1_1","CFir0_0","CFir1_0","CFir0_1","CFir1_1"]
    single_fault = ["SAFs0","SAFs1","TFs0","TFs1","WDFs0","WDFs1","RDFs0","RDFs1","IRFs0","IRFs1","DRDFs0","DRDFs1"]
    all_fault = coupling_fault + single_fault

    fp1 = fault_coverage[0][0]
    fp2 = coupling_fault[0]     #need to change for different list
    fp1_list = all_fault   #need to change for different list
    fp2_list = all_fault   #need to change for different list
    
    dic = {}
    line = []
    line.append("fp1/fp2")
    line.extend(fp2_list)
    csv_write.writerow(line)
    line.clear()
    for comb in fault_coverage:
        dic[comb[0]+comb[1]] = str(comb[2])+"%"+str(comb[3])
    for row in fp1_list:
        line.append(row)
        for column in fp2_list:
            line.append(dic.setdefault(row+column, ))
        csv_write.writerow(line)
        line.clear()

    
        


