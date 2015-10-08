import csv
import ep_classifier

# we have two classes and two sets of rules for each class
data_class0 = [['1', ['2', '4'], '3'], ['1', '4', '3'], ['1', '3', '4'], ['5', '1', '3']]
data_class1 = [['3', '2', '1'], ['4', '3', '1', '2'], ['3', '2', '5'], ['5', '3', '2', '1']]

# then we need to convert this representation of rules into format for SMPF programm
ep_classifier.sequence_to_SPMF(data_class0, 'data/spmf/Seq_class0')
ep_classifier.sequence_to_SPMF(data_class1, 'data/spmf/Seq_class1')

# now we use spmf with some configuration to find some frequent rules
# conf
# Chose an algorithm: PrefixSpan
# input: data/spmf/Seq_class0
# output: data/spmf_output/class0_rules
# choose minsup: 50% for example
