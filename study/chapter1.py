# -*- coding: utf-8 -*-
# author: WangYun 
# time :2018/9/20 
import numpy as np
from collections import defaultdict
from operator import itemgetter


#First,how many rows contain our premise:that a person is buying apples




def calS(X,n_features):


    #print n_features
    #print X[:5]#every row is a purchase record,evey column is a product
    #five kinds of product
    #bread,milk,cheese,apple and banana
    valid_rules=defaultdict(int)
    invalid_rules=defaultdict(int)
    num_occurances=defaultdict(int)
    print(X)
    for sample in X:
        for premise in range(5):
            # 如果没有买这个商品，则跳过本次统计
            if sample[premise]==0:continue
            # 如果买这个商品，则统计发生次数+1
            num_occurances[premise]+=1
            # 在这5中商品之中
            for conclusion in range(n_features):
                # 如果是本商品，则跳过
                if premise==conclusion:continue
                # 如果这个人既买了conclusion这个商品，又买了统计的这个商品，记有效次数 + 1
                if sample[conclusion]==1:
                    valid_rules[(premise,conclusion)] += 1
                # 如果这个买了conclusion这个商品，但是没有买统计的这个商品，记无效次数 + 1
                else:
                    invalid_rules[(premise,conclusion)] += 1
    # 支持度就是有效次数
    support=valid_rules
    # 置信度的计算
    confidence=defaultdict(float)
    for premise,conclusion in valid_rules.keys():
        rule=(premise,conclusion)
        confidence[rule]=float(valid_rules[rule])/num_occurances[premise]    #这里需要将valid_rules的规则条目数从int转成float
    return support,confidence


def print_rule(premise,conclusion,support,confidence,features):
    premise_name=features[premise]
    conclusion_name=features[conclusion]
    print("Rule:If a person buys {0} they will also buy {1}".format(premise_name,conclusion_name))
    print("-Support:{0}".format(support[(premise,conclusion)]))
    print("-Confidence:{0:.3f}".format(confidence[(premise,conclusion)]))

if __name__ == '__main__':
    file = r'E:\Python\资料\基础资料\Python数据挖掘入门与实战\Code_REWRITE\Chapter 1\affinity_dataset.txt'
    X = np.loadtxt(file)
    n_samples,n_features=X.shape
    premise=1
    conclusion=3
    support,confidence=calS(X,n_features)
    features = ["bread", "milk", "cheese", "apples", "bananas"]
    print(support,confidence)
    print_rule(premise,conclusion,support,confidence,features)
    # sorted support的dict 按照第一个域值来排序，并按从大到小排序
    sorted_support = sorted(support.items(), key=itemgetter(1), reverse=True)
    for index in range(5):
        print("Rule # {0}".format(index + 1))
        premise, conclusion = sorted_support[index][0]
        print_rule(premise, conclusion, support, confidence, features)
    sorted_confidence = sorted(confidence.items(), key=itemgetter(1),reverse=True)
    for index in range(5):
        print("Rule # {0}".format(index + 1))
        premise, conclusion = sorted_confidence[index][0]
        print_rule(premise, conclusion, support, confidence, features)
