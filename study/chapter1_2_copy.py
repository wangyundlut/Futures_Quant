# -*- coding: utf-8 -*-
# author: WangYun 

from sklearn.datasets import load_iris
import numpy as np
from collections import defaultdict
from operator import itemgetter
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

def main():
    data = load_iris()
    x = data.data
    # 目标
    y_true = data.target
    # 这里是根据均值进行的特征分类
    x_d = np.array(x > np.mean(x,axis=0), dtype=int)
    # 根据OneR规则，分类
    clf = DecisionTreeClassifier(random_state=14)
    scores = cross_val_score(clf, x_d, y_true, scoring='accuracy')
    print("Accuracy is {0:.2f} %".format(np.mean(scores) * 100))

    predictos = {}
    errors = {}
    xd_train, xd_test, y_train, y_test = train_test_split(x_d, y_true, random_state=14)
    for feature in range(x_d.shape[1]):
        predictor, feature_error = OneRs(xd_train, y_train, feature)
        predictos[feature] = predictor
        errors[feature] = feature_error

    best_feature, best_error = sorted(errors.items(),key=itemgetter(1),reverse=False)[0]
    best_predictor = predictos[best_feature]
    model = {'feature':best_feature,
             'predictor':predictos[best_feature]}
    # 训练之后，进行测试集的测试
    y_predicted = predict(xd_test, model)
    accurancy = np.mean(y_predicted == y_test)*100
    print("accurancy is {0:.2f}%".format(accurancy))

def predict(x_test, model):
    feature = model['feature']
    predictor = model['predictor']
    y_predicted = np.array([predictor[int(sample[feature])] for sample in x_test])
    return y_predicted


# 根据OneR规则，特征属性和值来进行分类
def OneR(x_d, y_true, feature, value):
    class_feature = defaultdict(int)
    for sample,y in zip(x_d, y_true):
        if sample[feature] == value:
            class_feature[y] += 1
    best_class = sorted(class_feature.items(), key=itemgetter(1), reverse=True)[0][0]
    incorrect_predictions = [class_count for class_value, class_count in class_feature.items()
                             if class_value != best_class]
    error = sum(incorrect_predictions)
    return best_class, error

    # 统计根据某个特征进行
def OneRs(x_d, y_true, feature):
    values = set(x_d[:, feature])
    feature_error = 0
    predictors = {}
    for value in values:
        best_class, error = OneR(x_d, y_true, feature, value)
        feature_error += error
        predictors[value] = best_class
    return predictors, feature_error



if __name__ == '__main__':
    main()