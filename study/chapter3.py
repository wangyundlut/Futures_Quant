# -*- coding: utf-8 -*-
# author: WangYun 
# time :2018/9/28 

import pandas as pd
import os
import numpy as np
from collections import defaultdict
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

def main():
    file_name = r'E:\Python\资料\基础资料\Python数据挖掘入门与实战'
    data_filename = os.path.join(file_name, "nba.xlsx")
    dataset = pd.read_excel(data_filename,sheet_name='nba')
    # 数据日期格式问题
    dataset['Date'] = pd.to_datetime(dataset['Date'])
    # 修改表头
    dataset['HomeWin'] = dataset['VisitorPts'] < dataset['HomePts']
    y_true = dataset['HomeWin'].values
    # 创建字典，存储球队上次比赛的结果
    won_last = defaultdict(int)
    dataset.loc[0, "HomeLastWin"] = 0
    # 添加进原来的dataframe结构中去
    dataset.loc[0, "VisitorLastWin"] = 0

    # 遍历pandas数据的所有情况
    for index, row in dataset.iterrows():
        # 主队
        home_team = row["Home Team"]
        # 客队
        visitor_team = row["Visitor Team"]
        # 主队上次是否赢了
        row["HomeLastWin"] = won_last[home_team]
        # 客队上次是否赢了
        row["VisitorLastWin"] = won_last[visitor_team]

        dataset.loc[index] = row

        # 更新上次主队是否赢球
        won_last[home_team] = row["HomeWin"]
        # 更新上次客队是否赢球
        won_last[visitor_team] = not row["HomeWin"]

        #==========================决策树算法开始=================、
    clf = DecisionTreeClassifier(random_state=14)
    x_previouswins = dataset[['HomeLastWin', 'VisitorLastWin']].values
    scores = cross_val_score(clf, x_previouswins, y_true, scoring='accuracy')
    print("Accuracy is {0:.2f} %".format(np.mean(scores)*100))
    # min_samples_split:创建一个新节点至少需要的个体数量
    # min_samples_leaf:保留节点，每个节点至少应该包含的个体数量
    file_name = r'E:\Python\资料\基础资料\Python数据挖掘入门与实战'
    data_filename = os.path.join(file_name, "nba_add.txt")
    f = open(data_filename)
    lines = f.readlines()
    data_list = []
    for line in lines:
        data_list_tempe = line.split(',')
        data_list.append(data_list_tempe)
    # 这个转换做的漂亮！！！
    standings = pd.DataFrame(data_list[1:], columns=data_list[0])
    dataset["HomeTeamRanksHigher"] = 0
    for index, row in dataset.iterrows():
        home_team = row["Home Team"]
        visitor_team = row["Visitor Team"]
        if home_team == "New Orleans Pelicans":
            home_team = "New Orleans Hornets"
        elif visitor_team == "New Orleans Pelicans":
            visitor_team = "New Orleans Hornets"
        try:
            home_rank = standings[standings["Team"] == home_team]["Rk"].values[0]
            visitor_rank = standings[standings["Team"] == visitor_team]["Rk"].values[0]
            row["HomeTeamRanksHigher"] = int(home_rank > visitor_rank)
        except IndexError:
            print('what')

        dataset.loc[index] = row

    x_homehigher = dataset[["HomeLastWin", "VisitorLastWin", "HomeTeamRanksHigher"]].values
    clf = DecisionTreeClassifier(random_state=14)
    scores = cross_val_score(clf, x_homehigher, y_true, scoring='accuracy')
    print("Accuracy is {0:.2f} %".format(np.mean(scores) * 100))
    last_match_winner = defaultdict(int)
    dataset["HomeTeamWonLast"] = 0
    for index, row in dataset.iterrows():
        home_team = row["Home Team"]
        visitor_team = row["Visitor Team"]
        teams = tuple(sorted([home_team, visitor_team]))
        row["HomeTeamWonLast"] == 1 if last_match_winner[teams] == row["Home Team"] else 0
        dataset.loc[index] = row
        winner = row["Home Team"] if row["HomeWin"] else row["Visitor Team"]
        last_match_winner[teams] = winner
    x_lastwinner = dataset[["HomeTeamRanksHigher", "HomeTeamWonLast"]].values
    clf = DecisionTreeClassifier(random_state=14)
    scores = cross_val_score(clf, x_lastwinner, y_true, scoring='accuracy')
    print("Accuracy is {0:.2f} %".format(np.mean(scores) * 100))
    encoding = LabelEncoder()
    encoding.fit(dataset["Home Team"].values)
    home_teams = encoding.transform(dataset["Home Team"].values)
    visitor_teams = encoding.transform(dataset["Visitor Team"].values)
    x_teams = np.vstack([home_teams, visitor_teams]).T
    onehot = OneHotEncoder()
    x_teams_expanded = onehot.fit_transform(x_teams).todense()
    clf = DecisionTreeClassifier(random_state=14)
    scores = cross_val_score(clf, x_teams_expanded, y_true, scoring='accuracy')
    print("Accuracy is {0:.2f} %".format(np.mean(scores) * 100))
    #=======================随机森林===========================
    clf = RandomForestClassifier(random_state=14)
    scores = cross_val_score(clf, x_teams, y_true, scoring='accuracy')
    print("Accuracy is {0:.2f} %".format(np.mean(scores)*100))

    parameter_space = {
        "n_estimators":[100,],
        "criterion":["gini","entropy"],
        "min_samples_leaf":[2,4,6],
    }
    clf = RandomForestClassifier(random_state=14)
    grid = GridSearchCV(clf, parameter_space)
    grid.fit(x_teams, y_true)
    print("Accuracy : {0:.1f} %".format(grid.best_score_*100))
    pass


if __name__ == '__main__':
    main()