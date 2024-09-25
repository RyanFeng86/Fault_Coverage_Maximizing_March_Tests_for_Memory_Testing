import csv
from itertools import *

num_loc = 4

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

def search_dictinary(faultname, fault_type):
    fault = []
    if (fault_type == 'single'):
        fault.append(single_fault_dict[faultname]['type'])
        fault.append(single_fault_dict[faultname]['subtype'])
        fault.append(single_fault_dict[faultname]['init'])
        fault.append(single_fault_dict[faultname]['op'])
        fault.append("NA")
        fault.append("NA")
        fault.append(single_fault_dict[faultname]['final'])
        fault.append(single_fault_dict[faultname]['read'])
    elif (fault_type == 'couple'):
        fault.append(coupling_fault_dict[faultname]['type'])
        fault.append(coupling_fault_dict[faultname]['subtype'])
        fault.append(coupling_fault_dict[faultname]['aggr_init'])
        fault.append(coupling_fault_dict[faultname]['aggr_op'])
        fault.append(coupling_fault_dict[faultname]['vic_init'])
        fault.append(coupling_fault_dict[faultname]['vic_op'])
        fault.append(coupling_fault_dict[faultname]['vic_final'])
        fault.append(coupling_fault_dict[faultname]['vic_read'])
    return fault

with open('Fault_Plan.csv', newline='') as fault_plan:
    csv_reader = csv.reader(fault_plan)
    data = list(csv_reader)
    row_len = (len(data))

single_fault_dict = {}
coupling_fault_dict = {}
all_fault_dict = {}
for fault in data[1:43]:
    coupling_fault_dict[fault[0]+fault[1]] = {
    'type':fault[0],
    'subtype':fault[1],
    'aggr_init':fault[2],
    'aggr_op':fault[3],
    'vic_init':fault[4],
    'vic_op':fault[5],
    'vic_final':fault[6],
    'vic_read':fault[7]
    }
    all_fault_dict[fault[0]+fault[1]] = {
    'type':fault[0],
    'subtype':fault[1],
    'aggr_init':fault[2],
    'aggr_op':fault[3],
    'vic_init':fault[4],
    'vic_op':fault[5],
    'vic_final':fault[6],
    'vic_read':fault[7]
    }
for fault in data[43::]:
    single_fault_dict[fault[0]+fault[1]] = {
    'type':fault[0],
    'subtype':fault[1],
    'init':fault[2],
    'op':fault[3],
    'final':fault[6],
    'read':fault[7]
    }
    all_fault_dict[fault[0]+fault[1]] = {
    'type':fault[0],
    'subtype':fault[1],
    'aggr_init':fault[2],
    'aggr_op':fault[3],
    'vic_init':fault[2],
    'vic_op':fault[3],
    'vic_final':fault[6],
    'vic_read':fault[7]
    }

def fault_pair_analysis(fp1, fp2, counter):
    if fp1 in single_fault_dict:
        fp1_type = 'single'
    elif fp1 in coupling_fault_dict:
        fp1_type = 'couple'
    else:
        fp1_type = 'NA'
    if fp2 in single_fault_dict:
        fp2_type = 'single'
    elif fp2 in coupling_fault_dict:
        fp2_type = 'couple'
    else:
        fp1_type = 'NA'

    fp1_address = []
    fp2_address = []
    if(fp1_type == 'single'):
        for i in permutations(list(range(num_loc)), 1):
            fp1_address.append([fp1, i[0], i[0]])# [1]aggr_addr, [2]vic_addr
    elif(fp1_type == 'couple'):
        for i in permutations(list(range(num_loc)), 2):
            fp1_address.append([fp1, i[0], i[1]])

    if(fp2_type == 'single'):
        for i in permutations(list(range(num_loc)), 1):
            fp2_address.append([fp2, i[0], i[0]])
    elif(fp2_type == 'couple'):
        for i in permutations(list(range(num_loc)), 2):
            fp2_address.append([fp2, i[0], i[1]])

    total_fault = 0
    addr_compatible = 0
    addr_incompatible = 0
    value_compatible = 0
    value_incompatible = 0
    mask = 0
    not_mask = 0
    for addr1 in fp1_address:
        for addr2 in fp2_address:
            link_flag = 0
            total_fault = total_fault + 1
            if (addr1[2] != addr2[2] or (fp1 == fp2 and addr1[1]==addr2[1])):
                addr_incompatible = addr_incompatible + 1
            else:
                addr_compatible = addr_compatible + 1
                if (all_fault_dict[fp1]['vic_final'] == all_fault_dict[fp2]['vic_init'] or all_fault_dict[fp2]['vic_init'] == "NA"
                    or all_fault_dict[fp1]['vic_final'] == "x_bar" or all_fault_dict[fp2]['vic_final'] == "x_bar" or
                    all_fault_dict[fp2]['vic_final'] == all_fault_dict[fp1]['vic_init'] or all_fault_dict[fp1]['vic_init'] == "NA"):

                    value_compatible = value_compatible + 1

                    if ((all_fault_dict[fp1]['vic_init'] != all_fault_dict[fp1]['vic_final'] 
                        and all_fault_dict[fp2]['vic_init'] != all_fault_dict[fp2]['vic_final'])
                    or  (all_fault_dict[fp1]['vic_final'] == "x_bar" and all_fault_dict[fp2]['vic_final'] == "x_bar")):

                        if ((all_fault_dict[fp1]['vic_init'] == all_fault_dict[fp2]['vic_final'] 
                            and all_fault_dict[fp2]['vic_init'] == all_fault_dict[fp1]['vic_final']) 
                        or  (all_fault_dict[fp1]['vic_final'] == "x_bar" 
                            and all_fault_dict[fp1]['vic_init'] == all_fault_dict[fp2]['vic_final'])
                        or  (all_fault_dict[fp2]['vic_final'] == "x_bar" 
                            and all_fault_dict[fp2]['vic_init'] == all_fault_dict[fp1]['vic_final'])
                        or  (all_fault_dict[fp1]['vic_final'] == "x_bar"
                            and all_fault_dict[fp2]['vic_final'] == "x_bar")):
                            mask = mask + 1
                            link_flag = 1
                        else:
                            not_mask = not_mask + 1
                    elif (all_fault_dict[fp1]['vic_init'] == all_fault_dict[fp1]['vic_final'] 
                         and all_fault_dict[fp1]['vic_op'][0] == "w"): #fp1 : vic_init == vic_final
                        if (all_fault_dict[fp1]['vic_op'][1] == all_fault_dict[fp2]['vic_final'] 
                         or all_fault_dict[fp2]['vic_final'] == "x_bar"):
                            mask = mask + 1
                            link_flag = 1
                        else:
                            not_mask = not_mask + 1
                    elif (all_fault_dict[fp2]['vic_init'] == all_fault_dict[fp2]['vic_final'] 
                         and all_fault_dict[fp2]['vic_op'][0] == "w"): #fp2 : vic_init == vic_final
                        if (all_fault_dict[fp2]['vic_op'][1] == all_fault_dict[fp1]['vic_final'] 
                         or all_fault_dict[fp1]['vic_final'] == "x_bar"):
                            mask = mask + 1
                            link_flag = 1
                        else:
                            not_mask = not_mask + 1
                    else :
                        not_mask = not_mask + 1
                else:
                    value_incompatible = value_incompatible + 1
            if (link_flag == 1):
                counter[0] = counter[0] + 1
                csv_write.writerow(temp_list_gen(search_dictinary(fp1, fp1_type), addr1[1], addr1[2], counter[0]))
                csv_write.writerow(temp_list_gen(search_dictinary(fp2, fp2_type), addr2[1], addr2[2], counter[0]))

    link_condition = [total_fault,addr_compatible,value_compatible,mask]
    print ("totally fault number: " + str(total_fault) + "\naddress incompatible: "+ str(addr_incompatible)+"\naddress compatible: "+ str(addr_compatible))
    print ("\tvalue incompatible: " + str(value_incompatible) + "\n\tvalue compatible: "+str(value_compatible))
    print ("\t\t not masked:" + str(not_mask) + "\n\t\t linked:" + str(mask))
    return link_condition

head = [ "fault_type", "sub_type", "aggr_addr", "aggr_val", "aggr_op", "vic_addr", "vic_val", "vic_op",
        "final_vic_val", "read_vic_val", "Fault_ID"]
all_fault = data[1::]
analysis_dict = {}
with open('long_list.csv', 'w', newline='') as long_list:
    csv_write = csv.writer(long_list)
    csv_write.writerow(head)
    counter = [0,0]
    link_num = 0
    total_num = 0
    for i in combinations_with_replacement(list(range(len(all_fault))), 2):
        fp1 = all_fault[i[0]][0] + all_fault[i[0]][1]
        fp2 = all_fault[i[1]][0] + all_fault[i[1]][1]   
        result = fault_pair_analysis(fp1, fp2, counter)
        analysis_dict[fp1+fp2] = result
        link_num = link_num + result[3]
        total_num = total_num + result[0]
        #analysis_dict[fp1+fp2] = {'total':result[0], 'addr_com':result[1], 'val_com':result[2], 'link':result[3]}

print(str(link_num)+"/"+str(total_num))
print(str(link_num/total_num*100)+"%")

with open('fault_analysis.csv', 'w', newline='') as fault_analysis:
    csv_write = csv.writer(fault_analysis)
    line = []
    line.append('')
    for fault in all_fault:
        line.append(fault[0]+fault[1])
    csv_write.writerow(line)
    line.clear()
    for fp1 in all_fault:
        line.append(fp1[0]+fp1[1])
        for fp2 in all_fault:
            dickey = fp1[0]+fp1[1]+fp2[0]+fp2[1]
            line.append(str(analysis_dict.setdefault(dickey, "NNNN")[3])+"%"+
                        str(analysis_dict.setdefault(dickey, "NNNN")[1])+"%"+
                        str(analysis_dict.setdefault(dickey, "NNNN")[0])  )
        csv_write.writerow(line)
        line.clear()