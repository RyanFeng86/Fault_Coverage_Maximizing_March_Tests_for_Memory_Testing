# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 00:51:30 2020

@author: sinof
"""

from memory_simulator import Memory_sim

def March_test(march_element, memory, fault, line_num, f_count):
    elements = march_element.strip().split(" ")
    order = elements[0]
    operations = elements[1:]
    if (order == "up"):
        for i in range(0, len(memory)):
            for j in range(0, len(operations)):
                fp1_active = 0
                fp2_active = 0
                st_on_1 = 0
                st_on_2 = 0
                if ((operations[j] == fault[0][4] and
                        i == fault[0][2] and #[2]aggr addr [3]aggr val [4]aggr op [5]vic addr [6]vic val [7]vic op [8]vic final [9] read vic
                        (memory[fault[0][2]] == fault[0][3] or fault[0][3] == 'NA') and
                        (memory[fault[0][5]] == fault[0][6] or fault[0][6] == 'NA'))
                        or
                    (operations[j] == fault[0][7] and
                        i == fault[0][5] and
                        (memory[fault[0][2]] == fault[0][3] or fault[0][3] == 'NA') and
                        (memory[fault[0][5]] == fault[0][6] or fault[0][6] == 'NA'))
                        or
                    (fault[0][4] == 'NA' and fault[0][7] == 'NA' and 
                      (i == fault[0][2] or i == fault[0][5]))):                    
                    fp1_active = 1
                    if (fault[0][4] == 'NA' and fault[0][7] == 'NA' and 
                      (i == fault[0][2] or i == fault[0][5])):
                        st_on_1 = 1
                        
                if ((operations[j] == fault[1][4] and
                        i == fault[1][2] and
                        (memory[fault[1][2]] == fault[1][3] or fault[1][3] == 'NA') and
                        (memory[fault[1][5]] == fault[1][6] or fault[1][6] == 'NA'))
                        or
                    (operations[j] == fault[1][7] and
                        i == fault[1][5] and
                        (memory[fault[1][2]] == fault[1][3] or fault[1][3] == 'NA') and
                        (memory[fault[1][5]] == fault[1][6] or fault[1][6] == 'NA'))
                        or
                    (fault[1][4] == 'NA' and fault[1][7] == 'NA' and 
                      (i == fault[1][2] or i == fault[1][5]))):  
                    fp2_active = 1
                    if (fault[1][4] == 'NA' and fault[1][7] == 'NA' and 
                      (i == fault[1][2] or i == fault[1][5])):
                        st_on_2 = 1
                
                if (fp1_active or fp2_active):
                    Memory_sim(operations[j], memory, i)
                
                if (fp1_active and fp2_active):
                    if (fault[0][8] == 'x_bar'):
                        memory[fault[0][5]] = str(int(memory[fault[0][5]]) ^ 1)
                    elif (st_on_1 and (memory[fault[0][2]] == fault[0][3])):
                        memory[fault[0][5]] = fault[0][8]
                    elif (st_on_1 == 0):
                        memory[fault[0][5]] = fault[0][8]                      
                    if (fault[1][8] == 'x_bar'):
                        memory[fault[1][5]] = str(int(memory[fault[1][5]]) ^ 1)
                    elif (st_on_2 and (memory[fault[1][2]] == fault[1][3])):
                        memory[fault[1][5]] = fault[1][8]
                    elif (st_on_2 == 0):
                        memory[fault[1][5]] = fault[1][8]
#                    print(fault[0][0]," and ", fault[1][0], "two faults activated at memory location", i, "at operation", operations[j])
                    if ((st_on_1 == 0) and (operations[j] == 'r0' and fault[0][9] == '1' and fault[0][5] == i) or (operations[j] == 'r1' and fault[0][9] == '0' and fault[0][5] == i)):
                        f_count = f_count + 1
                        return f_count    
                    elif ((st_on_1 == 1) and (operations[j] == 'r0' and memory[i] == '1' and fault[0][5] == i) or (operations[j] == 'r1' and memory[i] == '0' and fault[0][5] == i)):
                        f_count = f_count + 1
                        return f_count
                    elif ((st_on_2 == 0) and (operations[j] == 'r0' and fault[1][9] == '1' and fault[1][5] == i) or (operations[j] == 'r1' and fault[1][9] == '0' and fault[1][5] == i)):
                        f_count = f_count + 1
                        return f_count
                    elif ((st_on_2 == 1) and (operations[j] == 'r0' and memory[i] == '1' and fault[1][5] == i) or (operations[j] == 'r1' and memory[i] == '0' and fault[1][5] == i)):
                        f_count = f_count + 1
                        return f_count  
                    
                elif(fp1_active):
                    if (fault[0][8] == 'x_bar'):
                        memory[fault[0][5]] = str(int(memory[fault[0][5]]) ^ 1)
                    elif (st_on_1 and (memory[fault[0][2]] == fault[0][3])):
                        memory[fault[0][5]] = fault[0][8]
                    elif (st_on_1 == 0):
                        memory[fault[0][5]] = fault[0][8]
#                    print(fault[0][0], "fault activated at memory location", i, "at operation", operations[j])
                    if ((st_on_1 == 0) and (operations[j] == 'r0' and fault[0][9] == '1' and fault[0][5] == i) or (operations[j] == 'r1' and fault[0][9] == '0' and fault[0][5] == i)):
                        f_count = f_count + 1                    
                        return f_count
                    elif ((st_on_1 == 1) and (operations[j] == 'r0' and memory[i] == '1' and fault[0][5] == i) or (operations[j] == 'r1' and memory[i] == '0' and fault[0][5] == i)):
                        f_count = f_count + 1
                        return f_count
                    
                    
                elif(fp2_active):
                    if (fault[1][8] == 'x_bar'):
                        memory[fault[1][5]] = str(int(memory[fault[1][5]]) ^ 1)
                    elif (st_on_2 and (memory[fault[1][2]] == fault[1][3])):
                        memory[fault[1][5]] = fault[1][8]
                    elif (st_on_2 == 0):
                        memory[fault[1][5]] = fault[1][8]
#                    print(fault[1][0], "fault activated at memory location", i, "at operation", operations[j])
                    if ((st_on_2 == 0) and (operations[j] == 'r0' and fault[1][9] == '1' and fault[1][5] == i) or (operations[j] == 'r1' and fault[1][9] == '0' and fault[1][5] == i)):
                        f_count = f_count + 1
                        return f_count
                    elif ((st_on_2 == 1) and (operations[j] == 'r0' and memory[i] == '1' and fault[1][5] == i) or (operations[j] == 'r1' and memory[i] == '0' and fault[1][5] == i)):
                        f_count = f_count + 1
                        return f_count 

                elif ((Memory_sim(operations[j], memory, i) == 1)):
                    f_count = f_count + 1
                    #print("Error in March Test : " + str(line_num + 1) + " , in Operation : " + str(
                        #operations[j]) + " (Operation Num = " + str(j + 1) + ") at index = " + str(i))
                    return f_count
                else:
                    Memory_sim(operations[j], memory, i)


    else:
        for i in range(len(memory) - 1, -1, -1):
            for j in range(0, len(operations)):
                fp1_active = 0
                fp2_active = 0
                st_on_1 = 0
                st_on_2 = 0
                if ((operations[j] == fault[0][4] and
                        i == fault[0][2] and #[2]aggr addr [3]aggr val [4]aggr op [5]vic addr [6]vic val [7]vic op [8]vic final [9] read vic
                        (memory[fault[0][2]] == fault[0][3] or fault[0][3] == 'NA') and
                        (memory[fault[0][5]] == fault[0][6] or fault[0][6] == 'NA'))
                        or
                    (operations[j] == fault[0][7] and
                        i == fault[0][5] and
                        (memory[fault[0][2]] == fault[0][3] or fault[0][3] == 'NA') and
                        (memory[fault[0][5]] == fault[0][6] or fault[0][6] == 'NA'))
                        or
                    (fault[0][4] == 'NA' and fault[0][7] == 'NA' and 
                      (i == fault[0][2] or i == fault[0][5]))):                    
                    fp1_active = 1
                    if (fault[0][4] == 'NA' and fault[0][7] == 'NA' and 
                      (i == fault[0][2] or i == fault[0][5])):
                        st_on_1 = 1
                        
                if ((operations[j] == fault[1][4] and
                        i == fault[1][2] and
                        (memory[fault[1][2]] == fault[1][3] or fault[1][3] == 'NA') and
                        (memory[fault[1][5]] == fault[1][6] or fault[1][6] == 'NA'))
                        or
                    (operations[j] == fault[1][7] and
                        i == fault[1][5] and
                        (memory[fault[1][2]] == fault[1][3] or fault[1][3] == 'NA') and
                        (memory[fault[1][5]] == fault[1][6] or fault[1][6] == 'NA'))
                        or
                    (fault[1][4] == 'NA' and fault[1][7] == 'NA' and 
                      (i == fault[1][2] or i == fault[1][5]))):  
                    fp2_active = 1
                    if (fault[1][4] == 'NA' and fault[1][7] == 'NA' and 
                      (i == fault[1][2] or i == fault[1][5])):
                        st_on_2 = 1
                
                if (fp1_active or fp2_active):
                    Memory_sim(operations[j], memory, i)
                
                if (fp1_active and fp2_active):
                    if (fault[0][8] == 'x_bar'):
                        memory[fault[0][5]] = str(int(memory[fault[0][5]]) ^ 1)
                    elif (st_on_1 and (memory[fault[0][2]] == fault[0][3])):
                        memory[fault[0][5]] = fault[0][8]
                    elif (st_on_1 == 0):
                        memory[fault[0][5]] = fault[0][8]                      
                    if (fault[1][8] == 'x_bar'):
                        memory[fault[1][5]] = str(int(memory[fault[1][5]]) ^ 1)
                    elif (st_on_2 and (memory[fault[1][2]] == fault[1][3])):
                        memory[fault[1][5]] = fault[1][8]
                    elif (st_on_2 == 0):
                        memory[fault[1][5]] = fault[1][8]
#                    print(fault[0][0]," and ", fault[1][0], "two faults activated at memory location", i, "at operation", operations[j])
                    if ((st_on_1 == 0) and (operations[j] == 'r0' and fault[0][9] == '1' and fault[0][5] == i) or (operations[j] == 'r1' and fault[0][9] == '0' and fault[0][5] == i)):
                        f_count = f_count + 1
                        return f_count    
                    elif ((st_on_1 == 1) and (operations[j] == 'r0' and memory[i] == '1' and fault[0][5] == i) or (operations[j] == 'r1' and memory[i] == '0' and fault[0][5] == i)):
                        f_count = f_count + 1
                        return f_count
                    elif ((st_on_2 == 0) and (operations[j] == 'r0' and fault[1][9] == '1' and fault[1][5] == i) or (operations[j] == 'r1' and fault[1][9] == '0' and fault[1][5] == i)):
                        f_count = f_count + 1
                        return f_count
                    elif ((st_on_2 == 1) and (operations[j] == 'r0' and memory[i] == '1' and fault[1][5] == i) or (operations[j] == 'r1' and memory[i] == '0' and fault[1][5] == i)):
                        f_count = f_count + 1
                        return f_count  
                    
                elif(fp1_active):
                    if (fault[0][8] == 'x_bar'):
                        memory[fault[0][5]] = str(int(memory[fault[0][5]]) ^ 1)
                    elif (st_on_1 and (memory[fault[0][2]] == fault[0][3])):
                        memory[fault[0][5]] = fault[0][8]
                    elif (st_on_1 == 0):
                        memory[fault[0][5]] = fault[0][8]
#                    print(fault[0][0], "fault activated at memory location", i, "at operation", operations[j])
                    if ((st_on_1 == 0) and (operations[j] == 'r0' and fault[0][9] == '1' and fault[0][5] == i) or (operations[j] == 'r1' and fault[0][9] == '0' and fault[0][5] == i)):
                        f_count = f_count + 1                    
                        return f_count
                    elif ((st_on_1 == 1) and (operations[j] == 'r0' and memory[i] == '1' and fault[0][5] == i) or (operations[j] == 'r1' and memory[i] == '0' and fault[0][5] == i)):
                        f_count = f_count + 1
                        return f_count
                    
                    
                elif(fp2_active):
                    if (fault[1][8] == 'x_bar'):
                        memory[fault[1][5]] = str(int(memory[fault[1][5]]) ^ 1)
                    elif (st_on_2 and (memory[fault[1][2]] == fault[1][3])):
                        memory[fault[1][5]] = fault[1][8]
                    elif (st_on_2 == 0):
                        memory[fault[1][5]] = fault[1][8]
#                    print(fault[1][0], "fault activated at memory location", i, "at operation", operations[j])
                    if ((st_on_2 == 0) and (operations[j] == 'r0' and fault[1][9] == '1' and fault[1][5] == i) or (operations[j] == 'r1' and fault[1][9] == '0' and fault[1][5] == i)):
                        f_count = f_count + 1
                        return f_count
                    elif ((st_on_2 == 1) and (operations[j] == 'r0' and memory[i] == '1' and fault[1][5] == i) or (operations[j] == 'r1' and memory[i] == '0' and fault[1][5] == i)):
                        f_count = f_count + 1
                        return f_count 

                elif ((Memory_sim(operations[j], memory, i) == 1)):
                    f_count = f_count + 1
                    #print("Error in March Test : " + str(line_num + 1) + " , in Operation : " + str(
                        #operations[j]) + " (Operation Num = " + str(j + 1) + ") at index = " + str(i))
                    return f_count
                else:
                    Memory_sim(operations[j], memory, i)                
    return f_count