# -*- coding: utf-8 -*-
# author: WangYun 
# time :2018/10/25 

from selenium import webdriver

# 决策树，基尼不纯度，范芳铭
# 参考《集体智慧编程》
my_data = [['fan', 'C', 'yes', 32, 'None'],
           ['fang', 'U', 'yes', 23, 'Premium'],
           ['ming', 'F', 'no', 28, 'Basic']]


# 计算每一行数据的可能数量
def uniqueCounts(rows):
    results = {}
    for row in rows:
        # 对最后一列的值计算
        # r = row[len(row) - 1]
        # 对倒数第三的值计算，也就是yes 和no 的一列
        r = row[len(row) - 3]
        if r not in results: results[r] = 0
        results[r] += 1
    return results


# 基尼不纯度样例
def giniImpurityExample(rows):
    total = len(rows)
    print(total)
    counts = uniqueCounts(rows)
    print(counts)
    imp = 0
    for k1 in counts:
        p1 = float(counts[k1]) / total
        print(counts[k1])
        for k2 in counts:
            if k1 == k2: continue
            p2 = float(counts[k2]) / total
            imp += p1 * p2
    return imp

def main():
    gini = giniImpurityExample(my_data)
    print("gini Impurity is {}".format(gini))



if __name__ == '__main__':
    main()