import ep_classifier

data_class0 = [['1', ['2', '4'], '3'], ['1', '4', '3'], ['1', '3', '4'], ['5', '1', '3']]
data_class1 = [['3', '2', '1'], ['4', '3', '1', '2'], ['3', '2', '5'], ['5', '3', '2', '1']]

# read rules from SPMF output
# now we have some rules
class0_rules = ep_classifier.from_spmf_to_rules('data/spmf_output/class0_rules')
class1_rules = ep_classifier.from_spmf_to_rules('data/spmf_output/class1_rules')

# now we want to find most important rules for classification and their contribution to classification
dic_class0, dic_rules_class0 = ep_classifier.dict_of_contributions(class0_rules, data_class0, data_class1, 10)
dic_class1, dic_rules_class1 = ep_classifier.dict_of_contributions(class1_rules, data_class1, data_class0, 10)

print "Rules and contribution"
print dic_class0
print dic_rules_class0
print ""
print dic_class1
print dic_rules_class1
print ""

# we can classifiy a new pbject by using this rules
new_object1 = ['1', '2', '4', '1']
print "new_object1 classified as class" + \
      str(ep_classifier.classify_one_object(new_object1, dic_class0, dic_rules_class0, dic_class1, dic_rules_class1))
# new_object1 was classified as calss0, as it has rule [['1'], ['4']] and it's more important than rule [['2'], ['1']]
# from class1

new_object2 = ['1', '3', '2', '1']
print "new_object2 classified as class" + \
      str(ep_classifier.classify_one_object(new_object2, dic_class0, dic_rules_class0, dic_class1, dic_rules_class1))
# new_object2 was classified as class1, as it has rule [['2'], ['1']] and rule [['3'], ['2']] it's more important
# than rule [['1'], ['3']] from class1
