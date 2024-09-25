import csv

fault_type = 0
sub_type = 1
aggr_addr = 2
aggr_val = 3
aggr_op = 4
vic_addr = 5
vic_val = 6
vic_op = 7
final_vic_val = 8
read_vic_val = 9
fault_id = 10


class Memory:
    def __init__(self, mem_size):
        self.mem = ['' for i in range(0, mem_size)]
        self.mem_size = mem_size
        self.fault_detected = False

    def print_mem(self):
        print(self.mem)

    def write(self, location, value):
        self.mem[location] = value

    def read(self, location, value):
        if self.mem[location] != value:
            print('fault detected at location {}, expect to read {}'.format(location, value))
            self.fault_detected = True
            self.print_mem()


class MemorySim(Memory):
    def __init__(self, mem_size):
        Memory.__init__(self, mem_size)
        self.mem_size = mem_size
        self.fault_list = []
        self.fault_coverage = dict()
        self.saf_excited = []
        self.cfst_excited = []

    def inject_fault(self, fault_list):
        self.fault_list = fault_list
        for fault in self.fault_list:
            print('{} {}{} is injected'.format(fault[fault_id], fault[fault_type], fault[sub_type]))

    def stuck_fault(self, location):
        if self.saf_excited != [] and location == self.saf_excited[vic_addr]:
            return True
        if self.cfst_excited != [] and location == self.cfst_excited[vic_addr] and \
                self.mem[aggr_addr] == self.cfst_excited[aggr_val]:
            return True
        return False

    def run_march_test(self, march_test):
        for i, march_element in enumerate(march_test.strip().split(',')):
            self.run_march_element(march_element)
            print("march element {} has finished, memory now is".format(i + 1))
            self.print_mem()

    def run_march_element(self, march_element):
        order = march_element.strip().split(' ')[0]
        operations = march_element.strip().split(' ')[1:]
        if order == 'up':
            for i in range(0, self.mem_size):
                for op in operations:
                    if not self.excite_fault(i, op):
                        if op[0] == 'w' and not self.stuck_fault(i):
                            self.write(i, op[1])
                        if op[0] == 'r':
                            self.read(i, op[1])
        else:
            for i in reversed(range(self.mem_size)):
                for op in operations:
                    if not self.excite_fault(i, op):
                        if op[0] == 'w' and not self.stuck_fault(i):
                            self.write(i, op[1])
                        if op[0] == 'r':
                            self.read(i, op[1])

    def excite_fault(self, location, op):
        for fault in self.fault_list:
            if fault[aggr_addr] == fault[vic_addr]:  # single fault
                if location == fault[aggr_addr]:  # check aggr_addr
                    if self.mem[location] == fault[aggr_val] or fault[aggr_val] == 'NA':  # check aggr_val
                        if op[0] == 'w' and op == fault[aggr_op]:  # check write aggr_op
                            self.write(fault[vic_addr], fault[final_vic_val])  # update vic
                            return True
                        if op[0] == 'r' and fault[aggr_op][0] == 'r':  # check read aggr_op
                            self.write(fault[vic_addr], fault[final_vic_val])  # update vic
                            if op[1] != fault[read_vic_val]:
                                print('fault detected at location {}, expect to read {}'.format(location, op[1]))
                                self.print_mem()
                                self.fault_detected = True
                            return True
            else:  # coupling fault
                if fault[aggr_op] != 'NA':  # CFin/CFid
                    if location == fault[aggr_addr]:  # check aggr_addr
                        if self.mem[location] == fault[aggr_val]:  # check aggr_val
                            if self.mem[fault[vic_addr]] == fault[vic_val]:  # check vic_val of CFid
                                if op[0] == 'w' and op == fault[aggr_op]:  # check write aggr_op
                                    self.write(fault[vic_addr], fault[final_vic_val])  # update vic
                                    self.write(fault[aggr_addr], op[1])  # update aggr
                                    return True
                                if op[0] == 'r' and fault[aggr_op][0] == 'r':  # check read aggr_op
                                    self.write(fault[vic_addr], fault[final_vic_val])  # update vic
                                    self.read(fault[aggr_addr], op[1])
                                    return True
                            if fault[vic_val] == 'NA':  # check vic_val of CFin
                                if op[0] == 'w' and op == fault[aggr_op]:  # check write aggr_op
                                    self.write(fault[vic_addr], str(int(self.mem[fault[vic_addr]]) ^ 1))  # update vic
                                    self.write(fault[aggr_addr], op[1])  # update aggr
                                    return True
                if fault[vic_op] != 'NA':  # CFtr/CFwd/CFrd/CFdr/CFir
                    if location == fault[vic_addr]:  # check vic_addr
                        if self.mem[location] == fault[vic_val]:  # check vic_val
                            if self.mem[fault[aggr_addr]] == fault[aggr_val]:  # check aggr_val
                                if op[0] == 'w' and op == fault[vic_op]:  # check write vic_op
                                    self.write(fault[vic_addr], fault[final_vic_val])  # update vic
                                    return True
                                if op[0] == 'r' and fault[vic_op][0] == 'r':  # check read vic_op
                                    self.write(fault[vic_addr], fault[final_vic_val])  # update vic
                                    if op[1] != fault[read_vic_val]:
                                        print(
                                            'fault detected at location {}, expect to read {}'.format(location, op[1]))
                                        self.print_mem()
                                        self.fault_detected = True
                                    return True
                if fault[aggr_op] == 'NA' and fault[vic_op] == 'NA':  # check CFst
                    if location == fault[aggr_addr]:  # check aggr_addr
                        if self.mem[location] == fault[aggr_val]:  # check aggr_val
                            if self.mem[fault[vic_addr]] == fault[vic_val]:  # check vic_val of CFst
                                self.write(fault[vic_addr], fault[final_vic_val])  # update vic
                                return True
                        if op[0] == 'w' and op[1] == fault[aggr_val]:
                            if self.mem[fault[vic_addr]] == fault[vic_val]:  # check vic_val of CFst
                                self.write(fault[vic_addr], fault[final_vic_val])  # update vic
                                self.write(fault[aggr_addr], op[1])  # update aggr
                                return True
                    if location == fault[vic_addr]:  # check vic_addr
                        if self.mem[location] == fault[vic_val]:  # check vic_val
                            if self.mem[fault[aggr_addr]] == fault[aggr_val]:  # check aggr_val of CFst
                                self.write(fault[vic_addr], fault[final_vic_val])  # update vic
                                return True
                        if op[0] == 'w' and op[1] == fault[vic_val]:
                            if self.mem[fault[aggr_addr]] == fault[aggr_val]:  # check aggr_val of CFst
                                self.write(fault[vic_addr], fault[final_vic_val])  # update vic
                                return True

        return False


def read_csv(file_name):
    with open(file_name, newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        data = list(csv_reader)
        for row in data[1::]:
            row[aggr_addr] = int(row[aggr_addr])
            row[vic_addr] = int(row[vic_addr])
        fault_plan = []
        if data[1][fault_id] != data[2][fault_id]:  # one fault
            for i in range(1, len(data), 1):
                fault_plan.append([data[i]])
        else:  # multi fault
            for i in range(1, len(data), 2):
                fault_plan.append([data[i], data[i + 1]])

        return fault_plan


def count_coverage(fault_list, fault_detected, dic):
    fault_comb = ''
    if len(fault_list) == 1:  # no fault_comb if only one fault presents
        fault_comb = fault_list[0][fault_type] + fault_list[0][sub_type]

    if len(fault_list) == 2:
        fault_comb = '{} {}'.format(fault_list[0][fault_type] + fault_list[0][sub_type],
                                    fault_list[1][fault_type] + fault_list[1][sub_type])

    if fault_comb in dic:
        dic[fault_comb][1] = dic[fault_comb][1] + 1
        if fault_detected:
            dic[fault_comb][0] = dic[fault_comb][0] + 1
    else:
        if fault_detected:
            dic[fault_comb] = [1, 1]
        else:
            dic[fault_comb] = [0, 1]


def write_table(dic):
    with open('LF2aa_coverage.csv', 'w', newline='') as csv_file:  # need to change manually for different list
        csv_writer = csv.writer(csv_file)
        coupling_fault = ["CFinUP", "CFinDOWN", "CFidUP0", "CFidUP1", "CFidDOWN0", "CFidDOWN1", "CFst0_0", "CFst1_0",
                          "CFst0_1", "CFst1_1", "CFds0r0_0", "CFds1r1_0", "CFds0r0_1", "CFds1r1_1", "CFds0w0_0",
                          "CFds0w1_0", "CFds1w0_0", "CFds1w1_0", "CFds0w0_1", "CFds0w1_1", "CFds1w0_1", "CFds1w1_1",
                          "CFtr0_0", "CFtr1_0", "CFtr0_1", "CFtr1_1", "CFwd0_0", "CFwd1_0", "CFwd0_1", "CFwd1_1",
                          "CFrd0_0", "CFrd1_0", "CFrd0_1", "CFrd1_1", "CFdrd0_0", "CFdrd1_0", "CFdrd0_1", "CFdrd1_1",
                          "CFir0_0", "CFir1_0", "CFir0_1", "CFir1_1"]
        single_fault = ["SAFs0", "SAFs1", "TFs0", "TFs1", "WDFs0", "WDFs1", "RDFs0", "RDFs1", "IRFs0", "IRFs1",
                        "DRDFs0", "DRDFs1"]
        fp1 = coupling_fault  # need to change manually for different list
        fp2 = coupling_fault  # need to change manually for different list

        csv_writer.writerow(['fp1/fp2'] + fp2)
        row = []
        for f1 in fp1:
            for f2 in fp2:
                fault_comb = '{} {}'.format(f1, f2)
                if fault_comb in dic:
                    row.append(dic[fault_comb])
                else:
                    row.append('')
            csv_writer.writerow([f1] + row)
            row.clear()


# ---------- main function ---------- #
file_name = './long_list.csv'
fault_plan = read_csv(file_name)
#fault_plan = fault_plan[108:120]
print(fault_plan)

memory_size = 4
march_test = 'up w0, up r0 w1, down r1 w0'

fault_coverage = dict()

for fault_list in fault_plan:
    MemTest = MemorySim(memory_size)
    MemTest.inject_fault(fault_list)
    MemTest.run_march_test(march_test)

    count_coverage(fault_list, MemTest.fault_detected, fault_coverage)

for key in list(fault_coverage.keys()):
    print(key, ':', fault_coverage[key])

write_table(fault_coverage)
