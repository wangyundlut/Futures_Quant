# -*- coding: utf-8 -*-
# author: WangYun 

from sklearn.datasets import load_iris
import numpy as np
from collections import defaultdict
from operator import itemgetter
from sklearn.model_selection import train_test_split

def main():
    # 1 导入数据集，X是150个sample的4个特征，Y是sample的分类情况，有三类，作为结果对照
    dataset = load_iris()
    X = dataset.data
    Y = dataset.target
    print(dataset.DESCR)
    # 2 将连续数据离散化，将平均值作为域值
    attribute_means = X.mean(axis=0)
    X_d = np.array(X >= attribute_means, dtype=int)
    # 3 实现OneR算法，X是特征集，y_true是分类信息，feature_index表示用第几个特征来分类，value表示特征值
    # 用第0列，值为0来分类
    predictors, total_error = train_on_feature(X_d, Y, 0)
    # 得到训练集train 和测试集test
    Xd_train, Xd_test, y_train, y_test = train_test_split(X_d, Y, random_state=14)
    all_predictors = {}
    erros = {}
    for features_index in range(Xd_train.shape[1]):
        predictors, total_error = train_on_feature(Xd_train, y_train, features_index)
        all_predictors[features_index] = predictors
        erros[features_index] = total_error
    best_features, best_error = sorted(erros.items(), key=itemgetter(1))[0]
    model = {'feature': best_features, 'predictor': all_predictors[best_features][0]}
# 这个函数统计了y类中，第feature_index个特征值为value的sample的个数
# 只用一列特征值来分类，用第feature_index = 0列, value = 0来划分
def train_feature_value(X, y_true, feature_index, value):
    class_counts = defaultdict(int)
    for sample, y in zip(X, y_true):
        if sample[feature_index] == value:
            class_counts[y] += 1
    sorted_class_counts = sorted(class_counts.items(),
                                 key=itemgetter(1),
                                 reverse=True)
    most_frequent_class = sorted_class_counts[0][0]
    incorrect_predictions = [class_count for class_value, class_count in class_counts.items()
                             if class_value != most_frequent_class]
    error = sum(incorrect_predictions)
    return most_frequent_class, error

# 对于某项特征，遍历每一个特征值，使用上述函数，得到预测结果和每个特征值的错误率
def train_on_feature(X, y_true, feature_index):
    values = set(X[:, feature_index])
    predictors = {}
    errors = []
    for current_value in values:
        most_frequent_class, error = train_feature_value(X, y_true, feature_index, current_value)
        predictors[current_value] = most_frequent_class
        errors.append(error)
    total_error = sum(errors)
    return predictors, total_error


if __name__ == '__main__':
    main()