# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 00:51:30 2020

@author: sinof
"""

from memory_simulator import Memory_sim

def March_test(march_element,memory,fault,line_num, f_count):
    elements = march_element.strip().split(" ")
    order = elements[0]
    operations = elements[1:]
    if (order == "up"):
        for i in range(0, len(memory)):
            for j in range(0, len(operations)):
                                
                if (operations[j] == fault[4] and 
                        i == fault[2] and 
                        (memory[fault[2]] == fault[3] or fault[3] == 'NA') and 
                        (memory[fault[5]] == fault[6] or fault[6] == 'NA')):  
                    Memory_sim(operations[j], memory, i)
                    if (fault[8] == 'x_bar'):
                        memory[fault[5]] = str(int(memory[fault[5]])^1)
                    else:
                        memory[fault[5]] = fault[8]
                    print(fault[0], "fault activated at memory location", i, "at operation", operations[j])
                    if ((operations[j] == 'r0' and fault[9] == '1' and fault[5] == i) or (operations[j] == 'r1' and fault[9] == '0' and fault[5] == i)):
                        f_count = f_count + 1
                        print("Error in March Test : "+str(line_num+1)+" , in Operation : "+str(operations[j])+" (Operation Num = "+str(j+1)+") at index = "+str(i))
                        return f_count
                    
                elif (operations[j] == fault[7] and 
                        i == fault[5] and 
                        (memory[fault[2]] == fault[3] or fault[3] == 'NA') and 
                        (memory[fault[5]] == fault[6] or fault[6] == 'NA')): 
                    Memory_sim(operations[j], memory, i)
                    if (fault[8] == 'x_bar'):
                        memory[fault[5]] = str(int(memory[fault[5]])^1)
                    else:
                        memory[fault[5]] = fault[8]
                    print(fault[0], "fault activated at memory location", i, "at operation", operations[j])
                    if ((operations[j] == 'r0' and fault[9] == '1' and fault[5] == i) or (operations[j] == 'r1' and fault[9] == '0' and fault[5] == i)):
                        f_count = f_count + 1
                        print("Error in March Test : "+str(line_num+1)+" , in Operation : "+str(operations[j])+" (Operation Num = "+str(j+1)+") at index = "+str(i))
                        return f_count

#added a condition where both ops are NA
                    
                elif (fault[4] == 'NA' and fault[7] == 'NA' and 
                      (i == fault[2] or i == fault[5])): 
                    Memory_sim(operations[j], memory, i)
                    if (memory[fault[2]] == fault[3]):
                        memory[fault[5]] = fault[8]
                        print(fault[0], "fault activated at memory location", i, "at operation", operations[j])
                    if ((operations[j] == 'r0' and memory[i] == '1' and fault[5] == i) or (operations[j] == 'r1' and memory[i] == '0' and fault[5] == i)):
                        f_count = f_count + 1
                        print("Error in March Test : "+str(line_num+1)+" , in Operation : "+str(operations[j])+" (Operation Num = "+str(j+1)+") at index = "+str(i))
                        return f_count

                    
                elif ((Memory_sim(operations[j], memory, i) == 1)):
                    f_count = f_count + 1
                    print("Error in March Test : "+str(line_num+1)+" , in Operation : "+str(operations[j])+" (Operation Num = "+str(j+1)+") at index = "+str(i))
                    return f_count
                else:
                    Memory_sim(operations[j], memory, i)
                    
                    
    else :
        for i in range(len(memory)-1,-1,-1):
            for j in range(0, len(operations)):
                
                if (operations[j] == fault[4] and 
                        i == fault[2] and 
                        (memory[fault[2]] == fault[3] or fault[3] == 'NA') and 
                        (memory[fault[5]] == fault[6] or fault[6] == 'NA')):  
                    Memory_sim(operations[j], memory, i)
                    if (fault[8] == 'x_bar'):
                        memory[fault[5]] = str(bool(memory[fault[5]])^1)
                    else:
                        memory[fault[5]] = fault[8]
                    print(fault[0], "fault activated at memory location", i, "at operation", operations[j])
                    if ((operations[j] == 'r0' and fault[9] == '1' and fault[5] == i) or (operations[j] == 'r1' and fault[9] == '0' and fault[5] == i)):
                        f_count = f_count + 1
                        print("Error in March Test : "+str(line_num+1)+" , in Operation : "+str(operations[j])+" (Operation Num = "+str(j+1)+") at index = "+str(i))
                        return f_count

                    
                elif (operations[j] == fault[7] and 
                        i == fault[5] and 
                        (memory[fault[2]] == fault[3] or fault[3] == 'NA') and 
                        (memory[fault[5]] == fault[6] or fault[6] == 'NA')): 
                    Memory_sim(operations[j], memory, i)
                    if (fault[8] == 'x_bar'):
                        memory[fault[5]] = str(int(memory[fault[5]])^1)
                    else:
                        memory[fault[5]] = fault[8]
                    print(fault[0], "fault activated at memory location", i, "at operation", operations[j])
                    if ((operations[j] == 'r0' and fault[9] == '1' and fault[5] == i) or (operations[j] == 'r1' and fault[9] == '0' and fault[5] == i)):
                        f_count = f_count + 1
                        print("Error in March Test : "+str(line_num+1)+" , in Operation : "+str(operations[j])+" (Operation Num = "+str(j+1)+") at index = "+str(i))
                        return f_count

                        
                elif (fault[4] == 'NA' and fault[7] == 'NA' and 
                      (i == fault[2] or i == fault[5])): 
                    Memory_sim(operations[j], memory, i)
                    if (memory[fault[2]] == fault[3]):
                        memory[fault[5]] = fault[8]
                        print(fault[0], "fault activated at memory location", i, "at operation", operations[j])
                    if ((operations[j] == 'r0' and memory[i] == '1' and fault[5] == i) or (operations[j] == 'r1' and memory[i] == '0' and fault[5] == i)):
                        f_count = f_count + 1
                        print("Error in March Test : "+str(line_num+1)+" , in Operation : "+str(operations[j])+" (Operation Num = "+str(j+1)+") at index = "+str(i))
                        return f_count


                
                    
                elif ((Memory_sim(operations[j], memory, i) == 1)):
                    f_count = f_count + 1
                    print("Error in March Test : "+str(line_num+1)+" , in Operation : "+str(operations[j])+" (Operation Num = "+str(j+1)+") at index = "+str(i))
                    return f_count
                else:
                    Memory_sim(operations[j], memory, i)
    return f_count