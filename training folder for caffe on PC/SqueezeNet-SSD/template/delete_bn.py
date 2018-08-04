#!/usr/bin/env python

# This py used to delete the bn layer from the prototxt file

file_in = './squeezenet_ssd_deploy_template.prototxt'
file_out = './squeezenet_ssd_deploy_merge_bn_template.prototxt'

key_str1 = '/bn'
key_str2 = '/scale'
line_range1 = 18
line_range2 = 23
Foundflag = False
line_num = 0
line_num_list1 = []
line_num_list2 = []

file = open(file_in, 'r')
wirte_file = open(file_out, 'w')

# record the row of line which should be deleted
while True:
    line_num += 1

    line = file.readline()

    # this line has key_str
    if line.find(key_str1) >= 0 and line.find('fire5/bn') < 0:
        line_num_list1.append(line_num)
    if line.find(key_str2) >= 0 and line.find('fire5/scale') < 0:
        line_num_list2.append(line_num)

    if not line:
        break

# initalize the parameters which have been used above
line_num = 0
file = open(file_in, 'r')

# wirte the line which don't have to delete
while True:
    flag = 0
    line_num += 1

    line = file.readline()

    # check if this line should be deleted
    # delete bn layer
    for i in line_num_list1:
        if line_num >= i - 1 and line_num <= i + line_range1 - 2:
            flag = 1

    # delete scale layer
    for i in line_num_list2:
        if line_num >= i - 1 and line_num <= i + line_range2 - 2:
            flag = 1

    # flag == 0 so wirte this line to another file
    if flag == 0:
        wirte_file.write(line)

    if not line:
        break

file.close()
