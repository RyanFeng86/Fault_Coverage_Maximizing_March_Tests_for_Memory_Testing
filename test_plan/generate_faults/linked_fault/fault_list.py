import csv
from itertools import *

num_loc = int(input("Enter the size of memory = "))
#num_loc = 4

with open('Fault_Plan.csv', newline='') as fault_plan:
    csv_reader = csv.reader(fault_plan)
    data = list(csv_reader)
    row_len = (len(data))

one_cell_fault = data[43::]
two_cell_fault = data[1:43]

def temp_list_gen(fault, aggr_addr, vic_addr, counter):
    temp_list = []
    temp_list.append(fault[0])  # fault type
    temp_list.append(fault[1])  # fault sub-type
    temp_list.append(aggr_addr) # aggressor address
    temp_list.append(fault[2])  # initial value of aggressor
    temp_list.append(fault[3])  # operation at aggressor
    temp_list.append(vic_addr)  # victim address
    temp_list.append(fault[4])  # initial value of victim
    temp_list.append(fault[5])  # operation at aggressor
    temp_list.append(fault[6])  # final value of victim
    temp_list.append(fault[7])  # read value on victim
    temp_list.append(counter)   # fault number count
    return temp_list


head = [ "fault_type", "sub_type", "aggr_addr", "aggr_val", "aggr_op", "vic_addr", "vic_val", "vic_op",
        "final_vic_val", "read_vic_val", "Fault_ID"]

with open('fault_list_single.csv', 'w', newline='') as fault_list:
    csv_write = csv.writer(fault_list)
    csv_write.writerow(head)
    counter = 1
    for fault in two_cell_fault:
        for i in permutations(list(range(num_loc)), 2):
            csv_write.writerow(temp_list_gen(fault, i[0], i[1], counter))
            counter = counter + 1
    for fault in one_cell_fault:
        for i in permutations(list(range(num_loc)), 1):
            csv_write.writerow(temp_list_gen(fault, i[0], i[0], counter))
            counter = counter + 1


#--------Unlinked Faults--------#
with open('fault_list_ULF2_ss.csv', 'w', newline='') as fault_list:
    csv_write = csv.writer(fault_list)
    csv_write.writerow(head)
    counter = 1
    for i in combinations_with_replacement(list(range(len(one_cell_fault))), 2):
        fault1 = one_cell_fault[i[0]]
        fault2 = one_cell_fault[i[1]]
        for j in list(permutations(list(range(num_loc)), 2)):
            csv_write.writerow(temp_list_gen(fault1, j[0], j[0], counter))
            csv_write.writerow(temp_list_gen(fault2, j[1], j[1], counter))
            counter = counter + 1


with open('fault_list_ULF2_cc.csv', 'w', newline='') as fault_list:
    csv_write = csv.writer(fault_list)
    csv_write.writerow(head)
    counter = 1
    for i in combinations_with_replacement(list(range(len(two_cell_fault))), 2):
        fault1 = two_cell_fault[i[0]]
        fault2 = two_cell_fault[i[1]]

        if fault1[3] == 'NA': 
            fault1_final_aggr_val=fault1[2]
        else:
            fault1_final_aggr_val=fault1[3][1]

        if fault2[3] == 'NA': 
            fault2_final_aggr_val=fault2[2]
        else:
            fault2_final_aggr_val=fault2[3][1]

        if (fault1[6] == fault2[2] and fault1_final_aggr_val == fault2[4]) or (fault2[6] == fault1[2] and fault2_final_aggr_val == fault1[4]):
            for j in permutations(list(range(num_loc)), 2):
                csv_write.writerow(temp_list_gen(fault1, j[0], j[1], counter))
                csv_write.writerow(temp_list_gen(fault2, j[1], j[0], counter))
                counter = counter + 1

with open('fault_list_ULF3_cs.csv', 'w', newline='') as fault_list:
    csv_write = csv.writer(fault_list)
    csv_write.writerow(head)
    counter = 1
    for i in permutations(list(range(len(two_cell_fault))), 1):
        for m in permutations(list(range(len(one_cell_fault))), 1):
            fault1 = two_cell_fault[i[0]]
            fault2 = one_cell_fault[m[0]]
            for j in permutations(list(range(num_loc)), 3):
                csv_write.writerow(temp_list_gen(fault1, j[0], j[1], counter))
                csv_write.writerow(temp_list_gen(fault2, j[2], j[2], counter))
                counter = counter + 1

with open('fault_list_ULF3_cc.csv', 'w', newline='') as fault_list:
    csv_write = csv.writer(fault_list)
    csv_write.writerow(head)
    counter = 1
    for i in combinations_with_replacement(list(range(len(two_cell_fault))), 2):
        fault1 = two_cell_fault[i[0]]
        fault2 = two_cell_fault[i[1]]
        if fault1[6] == fault2[2] or fault2[6] == fault1[2]:
            for j in permutations(list(range(num_loc)), 3):
                csv_write.writerow(temp_list_gen(fault1, j[0], j[1], counter))
                csv_write.writerow(temp_list_gen(fault2, j[1], j[2], counter))
                counter = counter + 1

with open('fault_list_ULF3_cc2.csv', 'w', newline='') as fault_list:
    csv_write = csv.writer(fault_list)
    csv_write.writerow(head)
    counter = 1
    for i in combinations_with_replacement(list(range(len(two_cell_fault))), 2):
        fault1 = two_cell_fault[i[0]]
        fault2 = two_cell_fault[i[1]]

        if fault1[3] == 'NA': 
            fault1_final_aggr_val=fault1[2]
        else:
            fault1_final_aggr_val=fault1[3][1]

        if fault2[3] == 'NA': 
            fault2_final_aggr_val=fault2[2]
        else:
            fault2_final_aggr_val=fault2[3][1]

        if fault1_final_aggr_val == fault2[2] or fault2_final_aggr_val == fault1[2]:
            for j in permutations(list(range(num_loc)), 3):
                csv_write.writerow(temp_list_gen(fault1, j[1], j[0], counter))
                csv_write.writerow(temp_list_gen(fault2, j[1], j[2], counter))
                counter = counter + 1

with open('fault_list_ULF4.csv', 'w', newline='') as fault_list:
    csv_write = csv.writer(fault_list)
    csv_write.writerow(head)
    counter = 1
    for i in combinations_with_replacement(list(range(len(two_cell_fault))), 2):
        fault1 = two_cell_fault[i[0]]
        fault2 = two_cell_fault[i[1]]
        for j in permutations(list(range(num_loc)), 4):
            csv_write.writerow(temp_list_gen(fault1, j[0], j[1], counter))
            csv_write.writerow(temp_list_gen(fault2, j[2], j[3], counter))
            counter = counter + 1

            
#--------Linked Faults--------#
with open('fault_list_LF1.csv','w', newline='') as fault_list:
    csv_write = csv.writer(fault_list)
    csv_write.writerow(head)
    counter = 1
    for i in combinations_with_replacement(list(range(len(one_cell_fault))), 2):
        fault1 = one_cell_fault[i[0]]
        fault2 = one_cell_fault[i[1]]
        if fault1[6] == fault2[2] or fault2[6] == fault1[2]:
            for j in permutations(list(range(num_loc)), 1):
                csv_write.writerow(temp_list_gen(fault1, j[0], j[0], counter))
                csv_write.writerow(temp_list_gen(fault2, j[0], j[0], counter))
                counter = counter + 1

with open('fault_list_LF2_aa.csv','w', newline='') as fault_list:
    csv_write = csv.writer(fault_list)
    csv_write.writerow(head)
    counter = 1
    for i in combinations(list(range(len(two_cell_fault))), 2):
        fault1 = two_cell_fault[i[0]]
        fault2 = two_cell_fault[i[1]]
        if fault1[3] == 'NA': 
            fault1_final_aggr_val=fault1[2]
        else:
            fault1_final_aggr_val=fault1[3][1]

        if fault2[3] == 'NA': 
            fault2_final_aggr_val=fault2[2]
        else:
            fault2_final_aggr_val=fault2[3][1]

        if ((fault1_final_aggr_val == fault2[2] and fault1[6] == fault2[4]) or (fault2_final_aggr_val == fault1[2] and fault2[6] == fault1[4]) 
            or
            (fault1[6] == 'x_bar' and fault2[4] != fault2[6]) or (fault2[6] == 'x_bar' and fault1[4] != fault1[6])):
            for j in permutations(list(range(num_loc)), 2):
                csv_write.writerow(temp_list_gen(fault1, j[0], j[1], counter))
                csv_write.writerow(temp_list_gen(fault2, j[0], j[1], counter))
                counter = counter + 1

with open('fault_list_LF2_av.csv','w', newline='') as fault_list:
    csv_write = csv.writer(fault_list)
    csv_write.writerow(head)
    counter = 1
    for i in permutations(list(range(len(two_cell_fault))),1):
        for m in permutations(list(range(len(one_cell_fault))),1):
            fault1 = two_cell_fault[i[0]]
            fault2 = one_cell_fault[m[0]]
            if (fault1[6] == fault2[2] or fault2[6] == fault1[2]
                or
                fault1[6] == 'x_bar' and fault2[4] != fault2[6]):
                for j in permutations(list(range(num_loc)), 2):
                    csv_write.writerow(temp_list_gen(fault1, j[0], j[1], counter))
                    csv_write.writerow(temp_list_gen(fault2, j[1], j[1], counter))
                    counter = counter + 1

with open('fault_list_LF2_va.csv','w', newline='') as fault_list:
    csv_write = csv.writer(fault_list)
    csv_write.writerow(head)
    counter = 1
    for i in permutations(list(range(len(one_cell_fault))),1):
        for m in permutations(list(range(len(two_cell_fault))),1):
            fault1 = one_cell_fault[i[0]]
            fault2 = two_cell_fault[m[0]]
            if (fault1[6] == fault2[4] or fault2[6] == fault1[4]
                or
                fault2[6] == 'x_bar' and fault1[4] != fault1[6]):
                for j in permutations(list(range(num_loc)), 2):
                    csv_write.writerow(temp_list_gen(fault1, j[1], j[1], counter))
                    csv_write.writerow(temp_list_gen(fault2, j[0], j[1], counter))
                    counter = counter + 1

with open('fault_list_LF3.csv', 'w', newline='') as fault_list:
    csv_write = csv.writer(fault_list)
    csv_write.writerow(head)
    counter = 1
    for i in combinations_with_replacement(list(range(len(two_cell_fault))), 2):
        fault1 = two_cell_fault[i[0]]
        fault2 = two_cell_fault[i[1]]
        if (fault1[6] == fault2[4] or fault2[6] == fault1[4] or
            (fault1[6] == 'x_bar' and fault2[4] != fault2[6]) or (fault2[6] == 'x_bar' and fault1[4] != fault1[6])):
            for j in permutations(list(range(num_loc)), 3):
                csv_write.writerow(temp_list_gen(fault1, j[0], j[1], counter))
                csv_write.writerow(temp_list_gen(fault2, j[2], j[1], counter))
                counter = counter + 1