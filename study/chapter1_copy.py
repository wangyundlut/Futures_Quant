# -*- coding: utf-8 -*-
# author: WangYun 
# time :2018/9/20 
import numpy as np
from collections import defaultdict
from operator import itemgetter


#First,how many rows contain our premise:that a person is buying apples
# 计算买商品的置信度和支持度
def support_cal(X):
    # 首先看一共有多少个数据，有多少个特征
    n_samples, n_features = X.shape
    valid_rules = defaultdict(int)
    invalid_rules = defaultdict(int)
    num_occurances = defaultdict(int)
    # 大的循环，就是循环特征
    for feature in range(n_features):
        # 里面的小的循环，就是循环每个数据集
        for sample in X:
            # 计算各个情况发生的次数, 即置信度
            if sample[feature] == 1:
                num_occurances[feature] += 1
                # 根据特征情况，计算有效次数和无效次数，这就是支持度
                for premise in range(n_features):
                    # 如果自己统计自己，那么pass
                    if feature == premise: continue
                    # 如果规则有效，有效规则+1，如果规则无效，则无效+1
                    if sample[premise] == 1:
                        valid_rules[(feature, premise)] += 1
                    else:
                        invalid_rules[(feature, premise)] += 1
    # 对结果进行分析
    # 支持度
    support = valid_rules
    # 置信度
    confidence = defaultdict(float)
    for feature, premise in valid_rules.keys():
        rule = (feature, premise)
        confidence[rule] = float(valid_rules[rule])/num_occurances[feature]
    sorted(confidence.items(), key=itemgetter(1), reverse=True)
    return support, confidence

def print_rule(support, confidence, feature, conclusion):
    features = ['apple','banana','girl','boy','f_word']
    print("# buy {0}, also buy {1}".format(features[feature], features[conclusion]))
    print("-support: {0}".format(support[(feature, conclusion)]))
    print("-confidence: {0:.3f}".format(confidence[(feature, conclusion)]))



if __name__ == '__main__':
    file = r'E:\Python\资料\基础资料\Python数据挖掘入门与实战\Code_REWRITE\Chapter 1\affinity_dataset.txt'
    X = np.loadtxt(file)
    support, confidence = support_cal(X)
    # print_rule(support, confidence, 0, 3)
    support_sort = sorted(support.items(),key=itemgetter(1),reverse=True)
    for i in range(5):
        feature = support_sort[i][0][0]
        conclusion = support_sort[i][0][1]
        print_rule(support, confidence, feature, conclusion)

    confidence_sort = sorted(confidence.items(),key=itemgetter(1),reverse=True)
    for i in range(5):
        feature = confidence_sort[i][0][0]
        conclusion = confidence_sort[i][0][1]
        print_rule(support, confidence, feature, conclusion)




    pass

