import csv
from itertools import *

with open('Fault_Plan.csv', newline='') as fault_plan:
    csv_reader = csv.reader(fault_plan)
    data = list(csv_reader)
    row_len = (len(data))

one_cell_fault = data[43::]
two_cell_fault = data[1:43]

def head_gen(fault_list):
    head = []
    head.append("FP1\FP2")
    if fault_list == "one_cell_fault":
        for fault in one_cell_fault:
            head.append(fault[0]+fault[1])
    elif fault_list == "two_cell_fault":
        for fault in two_cell_fault:
            head.append(fault[0]+fault[1])
    return head

with open('LF1_table.csv', 'w', newline='') as LF1_table:
    csv_write = csv.writer(LF1_table)
    csv_write.writerow(head_gen("one_cell_fault"))
    row = []    
    for fp1 in one_cell_fault:
        row.clear()
        row.append(fp1[0]+fp1[1])
        for fp2 in one_cell_fault:
            judge = ""
            if fp1[2] != fp1[7] and fp1[3][0] == "r":
                judge = "D"
            elif fp1[6] == fp2[6]:
                judge = "~M"
            elif fp1[6] != fp2[2]:
                judge = "~C"
            elif fp1[3][1] != fp2[7] and fp2[3][0] == "r":
                judge = "D"
            else:
                judge = "L"

            if fp1[0] == 'SAFs' and judge == 'L':
                judge = "~M"

            row.append(judge)
        csv_write.writerow(row)
        
with open('LF2aa_table.csv', 'w', newline='') as LF2aa_table:
    csv_write = csv.writer(LF2aa_table)
    csv_write.writerow(head_gen("two_cell_fault"))
    row = []    
    for fp1 in two_cell_fault:
        row.clear()
        row.append(fp1[0]+fp1[1])

        if fp1[3] == "NA": 
            fp1_final_aggr_val=fp1[2]
        else:
            fp1_final_aggr_val=fp1[3][1]

        if fp1[5] == "NA":
            fp1_final_vic_val_exp=fp1[4]
        else:
            fp1_final_vic_val_exp=fp1[5][1]

        for fp2 in two_cell_fault:
            judge = ""
            if fp1[4] != fp1[7] and fp1[5][0] == "r":
                judge = "D"
            elif fp1[6] == fp2[6]:
                judge = "~M"
            elif fp1_final_aggr_val != fp2[2] or fp1[6] != fp2[4]:
                judge = "~C"
            elif fp1_final_vic_val_exp != fp2[7] and fp2[5][0] == "r":
                judge = "D"
            else:
                judge = "L"

            row.append(judge)
        csv_write.writerow(row)
                
with open('LF2av_table.csv', 'w', newline='') as LF2av_table:
    csv_write = csv.writer(LF2av_table)
    csv_write.writerow(head_gen("one_cell_fault"))
    row = []    
    for fp1 in two_cell_fault:
        row.clear()
        row.append(fp1[0]+fp1[1])

        if fp1[5] == "NA":
            fp1_final_vic_val_exp=fp1[4]
        else:
            fp1_final_vic_val_exp=fp1[5][1]

        for fp2 in one_cell_fault:
            judge = ""
            if fp1[4] != fp1[7] and fp1[5][0] == "r":
                judge = "D"
            elif fp1[6] == fp2[6]:
                judge = "~M"
            elif fp1[6] != fp2[2]:
                judge = "~C"
            elif fp1_final_vic_val_exp != fp2[7] and fp2[3][0] == "r":
                judge = "D"
            else:
                judge = "L"

            if fp2[0] == 'SAFs' and judge == 'L':
                judge = "~M"

            row.append(judge)
        csv_write.writerow(row)

with open('LF2va_table.csv', 'w', newline='') as LF2va_table:
    csv_write = csv.writer(LF2va_table)
    csv_write.writerow(head_gen("two_cell_fault"))
    row = []    
    for fp1 in one_cell_fault:
        row.clear()
        row.append(fp1[0]+fp1[1])

        for fp2 in two_cell_fault:
            judge = ""
            if fp1[2] != fp1[7] and fp1[3][0] == "r":
                judge = "D"
            elif fp1[6] == fp2[6]:
                judge = "~M"
            elif fp1[6] != fp2[4]:
                judge = "~C"
            elif fp1[3][1] != fp2[7] and fp2[5][0] == "r":
                judge = "D"
            else:
                judge = "L"

            if fp1[0] == 'SAFs' and judge == 'L':
                judge = "~M"

            row.append(judge)
        csv_write.writerow(row)

with open('LF3_table.csv', 'w', newline='') as LF3_table:
    csv_write = csv.writer(LF3_table)
    csv_write.writerow(head_gen("two_cell_fault"))
    row = []    
    for fp1 in two_cell_fault:
        row.clear()
        row.append(fp1[0]+fp1[1])

        if fp1[3] == "NA": 
            fp1_final_aggr_val=fp1[2]
        else:
            fp1_final_aggr_val=fp1[3][1]

        if fp1[5] == "NA":
            fp1_final_vic_val_exp=fp1[4]
        else:
            fp1_final_vic_val_exp=fp1[5][1]

        for fp2 in two_cell_fault:
            judge = ""
            if fp1[4] != fp1[7] and fp1[5][0] == "r":
                judge = "D"
            elif fp1[6] == fp2[6]:
                judge = "~M"
            elif fp1[6] != fp2[4]:
                judge = "~C"
            elif fp1_final_vic_val_exp != fp2[7] and fp2[5][0] == "r":
                judge = "D"
            else:
                judge = "L"

            row.append(judge)
        csv_write.writerow(row)
    
        