# -*- coding: utf-8 -*-
# author: WangYun 
# time :2018/9/30 

import os
import pandas as pd
import csv
from collections import defaultdict
import sys
from operator import itemgetter

def main():
    filename = r"E:\Python"
    ratings_filename = os.path.join(filename,"u.data")
    # padas读取csv文件，是要读取全英文目录的
    all_ratings = pd.read_csv(ratings_filename, delimiter="\t",header=None,
                              names=["UserID","MovieID","Rating","Datetime"])
    all_ratings["Datetime"] = pd.to_datetime(all_ratings["Datetime"],unit='s')
    # 提取喜欢的某一部电影
    all_ratings["Favorable"] = all_ratings["Rating"] > 3
    # 选取一部分数据用作训练集，有效减少搜索空间，提升Apriori算法速度
    ratings = all_ratings[all_ratings["UserID"].isin(range(200))]
    # 新建数据集，只包括用户喜欢某部电影的数据行
    favorable_ratings = ratings[ratings["Favorable"]]
    # 按照UserID进行分组，并遍历每个用户看过的每一部电影
    for k, v in favorable_ratings.groupby(["UserID","MovieID"]):
        print(k)
        print(frozenset(v.values[0]))
    # 根据UserID和MovieID分组，记录UserID，MovieID， 和
    favorable_reviews_by_users = dict((k, frozenset(v.values)) for k, v in favorable_ratings.groupby("UserID")["MovieID"])
    len(favorable_reviews_by_users)
    # 了解每部电影的影迷数量
    num_favorable_by_movie = ratings[["MovieID","Favorable"]].groupby("MovieID").sum()
    num_favorable_by_movie.sort_values("Favorable", ascending=False)[:5]

    #==================Apriori算法==============================
    # 频繁项集保存到以项集长度为键的字典中，根据长度查找
    frequent_itemsets = {}
    # 最小支持度
    min_support = 50
    frequent_itemsets[1] = dict((frozenset((movie_id,)), row["Favorable"])
                                for movie_id, row in num_favorable_by_movie.iterrows()
                                if row["Favorable"] > min_support)

    sys.stdout.flush()
    for k in range(2, 20):
        cur_frequent_itemsets = find_frequent_itemsets(favorable_reviews_by_users, frequent_itemsets[k-1],min_support)
        if len(cur_frequent_itemsets) == 0:
            print("did not find any {0}".format(k))
            sys.stdout.flush()
            break
        else:
            print("i found {0} frequent itemsets of length {1}".format(len(cur_frequent_itemsets), k))
            sys.stdout.flush()
            frequent_itemsets[k] = cur_frequent_itemsets
    del frequent_itemsets[1]
    # 抽取关联规则
    candidate_rules = []
    # 2,3，    frozenset({1,7}).....frozenset({1,50})
    for itemset_length, itemset_counts in frequent_itemsets.items():
        # ({1,7})
        for itemset in itemset_counts.keys():
            # conclusion只有一个，就是在。。。。存在的情况下，concolusion能够得到的概率
            for conclusion in itemset:
                # 前提就是全部的keys减去conlusion
                premise = itemset - set((conclusion,))
                candidate_rules.append((premise, conclusion))
    print(candidate_rules[:5])
    # 计算置信度
    correct_counts = defaultdict(int)
    incorrect_counts = defaultdict(int)
    # 遍历所有用户的喜好
    for user, reviews in favorable_reviews_by_users.items():
        # 遍历关联规则
        for candidate_rule in candidate_rules:
            premise, conclusion = candidate_rule
            # 看用户是否喜欢前提中的所有电影
            if premise.issubset(reviews):
                # 复合前提条件，看用户是否喜欢结论中的电影，如果是的话，适用规则，反之，规则不适用
                if conclusion in reviews:
                    correct_counts[candidate_rule] += 1
                else:
                    incorrect_counts[candidate_rule] += 1
    rule_canfidence = {candidate_rule:correct_counts[candidate_rule]/float(correct_counts[candidate_rule] + incorrect_counts[candidate_rule])
                       for candidate_rule in candidate_rules}
    # 前5个置信度比较高的
    sorted_confidence = sorted(rule_canfidence.items(), key=itemgetter(1), reverse=True)
    for index in range(5):
        print("Rule # {0}".format(index + 1))
        (premise, conclusion) = sorted_confidence[index][0]
        print("Rule: If a person recommands {0} they will also recommands {1}".format(premise, conclusion))
        print(" - Confidence: {0:.3f}".format((rule_canfidence[(premise, conclusion)])))
    pass
# 2用函数实现查找现有频繁项集的超集，发现新的频繁项集
# 3测试新生成的备选集的频繁程度，如果不够频繁，则舍弃。
def find_frequent_itemsets(favorable_reviews_by_users, k_1_itemsets, min_support):
    # 初始化字典
    counts = defaultdict(int)
    # 遍历所有用户和他们的打分情况
    for user, reviews in favorable_reviews_by_users.items():
        # 遍历前面找出的项集，判断他们是否是当前评分项集的子集。如果是，表明用户已经为子集中的电影打过分
        for itemset in k_1_itemsets:
            # 如果某用户看过要生成的超集中的需要遍历的那个
            if itemset.issubset(reviews):
                # 遍历用户打过分却没有出现在项集里的电影，用它生成超集，更新该项集的计数
                for other_reviewed_movie in reviews - itemset:
                    # 当前的超集等于遍历的那个加上新生成的一个
                    current_superset = itemset | frozenset((other_reviewed_movie,))
                    # 记录的数目增加
                    counts[current_superset] += 1
    # 如果满足最小支持度，则记录下来
    return dict([(itemset, frequency) for itemset ,frequency in counts.items() if frequency >= min_support])


if __name__ == '__main__':
    main()