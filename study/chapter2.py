# -*- coding: utf-8 -*-
# author: WangYun 


import os
import numpy as np
import csv
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline


def main():
    data_folder = r'E:\Python\资料\基础资料\Python数据挖掘入门与实战'
    # 这个函数很有用，合并文件名称
    data_filename = os.path.join(data_folder, "ionosphere" ,"ionosphere.data")
    # print(os.path.expanduser(('-')))
    x = np.zeros((351, 34), dtype='float')
    y = np.zeros((351, ), dtype='bool')
    with open(data_filename, 'r') as input_file:
        reader = csv.reader(input_file)
        # enumerate 是产生下标的一种方式
        for i ,row in enumerate(reader):
            # data是list，产生的方式就是float一下
            data = [float(datum) for datum in row[:-1]]
            x[i] = data
            y[i] = row[-1] == 'g'
    x_train, x_test, y_train, y_test = train_test_split(x, y,random_state=14)
    estimator = KNeighborsClassifier()
    estimator.fit(x_train, y_train)
    y_predicted = estimator.predict(x_test)
    accuracy = np.mean(y_test == y_predicted) * 100
    print("accuracy is {0:.1f} %".format(accuracy))

    # 用stratified K Fold方法切分数据集，大体保证切分后得到的子数据集中类别分布相同

    scores = cross_val_score(estimator, x, y, scoring='accuracy')
    average_accuracy = np.mean(scores)*100
    print("average accuracy is {0:.1f} %".format(average_accuracy))

    ave_scores = []
    all_scores = []
    parameter_values = list(range(1, 21))
    for n_neighbors in parameter_values:
        estimator = KNeighborsClassifier(n_neighbors=n_neighbors)
        scores = cross_val_score(estimator, x, y, scoring='accuracy')
        ave_scores.append(np.mean(scores))
        all_scores.append(scores)
    plt.plot(parameter_values, ave_scores, '-o')
    # 破坏数据
    x_broken = np.array(x)
    x_broken[:,::2]/=10
    # 对破坏的数据进行分类预测
    estimator = KNeighborsClassifier()
    orginal_scores = cross_val_score(estimator, x, y, scoring='accuracy')
    print("orginala accuracy is {0:.2f} %".format(np.mean(orginal_scores)*100))
    broken_scores = cross_val_score(estimator, x_broken, y, scoring='accuracy')
    print("broken accuracy is {0:.2f} %".format(np.mean(broken_scores)*100))

    # 数据预处理
    # 这里有最大值为1 最小值为0 的处理
    # 各项特征值的和为1 sklearn.preprocessing.Normalizer
    # 均值为0，方差为1， sklearn.preprocessing.StandardScaler
    # 特征的二值化，sklearn.preprocessing.Binarizer大于阈值为1，反之为0
    x_transformed = MinMaxScaler().fit_transform(x)
    estimator = KNeighborsClassifier()
    transformed_scores = cross_val_score(estimator, x_transformed, y, scoring='accuracy')
    print("{0:.2f} % ".format(np.mean(transformed_scores)*100))

    # 数据流水线结构
    # 最后一步必须是估计器，前几步是转换器。
    scalling_pipeline = Pipeline([('scale', MinMaxScaler()),
                                  ('predict', KNeighborsClassifier())])
    scores = cross_val_score(scalling_pipeline, x_broken, y, scoring='accuracy')
    print("{0:.1f} %".format(np.mean(scores)*100))
    pass


if __name__ == '__main__':
    main()