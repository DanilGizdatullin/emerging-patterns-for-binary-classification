import csv

INFINITY = 100

coding_dic = {'work': 1,
              'separation': 2,
              'partner': 3,
              'marriage': 4,
              'children': 5,
              'parting': 6,
              'divorce': 7,
              'education': 8}


def data_list_to_sequence_list2(data_list, names):
    # maps attributes to a sequence based on sorting them by age in an ascending order
    # taking into account equal ages

    sequence_list = []
    for row in data_list:
        temp_seq = sorted(row.keys(), key=row.get)
        sequence = []
        prev_ev = ''
        for ev in temp_seq:
            if prev_ev == '':
                sequence.append([str(coding_dic[ev])])
            elif row[prev_ev] == row[ev]:
                sequence[-1].append(str(coding_dic[ev]))
            else:
                sequence.append([str(coding_dic[ev])])
            prev_ev = ev
        sequence_list.append(sequence)

    return sequence_list


def sequence_to_SPMF(sequence_list, filename):
    #  recoding Sequence from our program type to SPMF readeble file

    outfile = open(filename+'.txt', 'w')

    for seq in sequence_list:
        for el in seq:
            if len(el) == 1:
                outfile.write(el[0]+' -1 ')
            else:
                for el2 in el:
                    outfile.write(el2+' ')
                outfile.write('-1 ')
        outfile.write('-2\n')

    print filename

    outfile.close()

    return []


def find_item_in_seq(item=1, sequence=[[1, 2], [3], [4], [5]]):
    # return number of object which has item 'a' or return -1

    sequence_l = len(sequence)
    flag = False
    cntr = 0
    ans = -1
    while (cntr < sequence_l) & (not flag):
        flag = (item in sequence[cntr])
        if flag:
            ans = cntr
            break
        else:
            cntr += 1
    return ans

# item = 1
# sequence = [[1, 2], [3], [4], [5]]


def find_elem_in_seq(elem, sequence):
    # function return number of object which has element 'a' or return -1

    elem_l = len(elem)
    flag = False
    pos1 = find_item_in_seq(elem[0], sequence)
    if pos1 != -1:
        flag = True
        for i in elem:
            if find_item_in_seq(i, [sequence[pos1]]) == -1:
                flag = False
                break
        if flag:
            return pos1
        else:
            return -1
    else:
        return -1

# elem = [5]
# sequence = [[1, 2], [3], [4], [5]]


def find_obj_in_seq(obj, sequence):
    # return True if object in sequence else return False

    obj_l = len(obj)
    sequence_l = len(sequence)
    if obj_l <= sequence_l:
        pos1 = find_elem_in_seq(obj[0], sequence)
        if (pos1 != -1) & (len(obj) == 1):
            return True
        elif pos1 != -1:
            return find_obj_in_seq(obj[1:], sequence[pos1+1:])
        else:
            return False
    else:
        return False


def support(rule, dataset):
    # return support for rule in some data

    cntr = 0
    for seq in dataset:
        if find_obj_in_seq(rule, seq):
            cntr += 1

    return cntr / float(len(dataset))


def growth_rate(rule, dataset1, dataset2):
    # function return growth-rate for rule and two datasets

    support_dataset1 = support(rule, dataset1)
    support_dataset2 = support(rule, dataset2)
    if (support_dataset1 == 0) & (support_dataset2 == 0):
        return 0
    elif (support_dataset1 != 0) & (support_dataset2 == 0):
        return INFINITY
    else:
        return support_dataset1 / support_dataset2


def dict_of_contributions(rules, dataset1, dataset2, threshold):
    # function to find the contributions of rules in classification task

    dict_of_contributions_to_score_class1 = {}
    dict_of_rules = {}

    for i in xrange(len(rules)):
        dict_of_rules[str(97+i)] = rules[i]

    for key in dict_of_rules.keys():

        gr_ra1 = growth_rate(dict_of_rules[key], dataset1, dataset2)

        if gr_ra1 > threshold:
            if gr_ra1 == INFINITY:
                dict_of_contributions_to_score_class1[key] = support(dict_of_rules[key], dataset1)
            else:
                dict_of_contributions_to_score_class1[key] = (gr_ra1/(1+gr_ra1)) * support(dict_of_rules[key], dataset1)
    return dict_of_contributions_to_score_class1, dict_of_rules


def from_spmf_to_rules(file_path):
    # fucntion which converts rules from SMPF output into our internal representation

    list_of_rules = []
    csvfile = open(file_path, 'r')
    sreader = csv.reader(csvfile, delimiter=' ')
    for row in sreader:
        rule = []
        i = 0
        rule_elem = []
        while row[i] != '#SUP:':
            if row[i] != '-1':
                rule_elem.append(row[i])
                i += 1
            else:
                rule.append(rule_elem)
                rule_elem = []
                i += 1
        list_of_rules.append(rule)
    return list_of_rules


def classify_one_object(object_to_classification, dic1, dic_rules1, dic2, dic_rules2):
    # function which classify one object
    # return 0 or 1 as class
    # return -1 when object can't be classified

    score_for_class1 = 0
    score_for_class2 = 0
    rules_from_first_class = []
    rules_from_second_class = []
    for key, value in dic_rules1.items():
        if find_obj_in_seq(value, object_to_classification):
            rules_from_first_class.append(key)
    for key, value in dic_rules2.items():
        if find_obj_in_seq(value, object_to_classification):
            rules_from_second_class.append(key)

    for rule in rules_from_first_class:
        if rule in dic1:
            score_for_class1 += dic1[rule]

    for rule in rules_from_second_class:
        if rule in dic2:
            score_for_class2 += dic2[rule]

    if (score_for_class1 == score_for_class2) and (score_for_class1 == 0):
        return -1
    elif score_for_class1 >= score_for_class2:
        return 0
    else:
        return 1
