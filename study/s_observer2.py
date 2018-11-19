#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
观察者和被观察者
以及两者之间的绑定
如果苹果树病了，种树的人要去治疗树，否则什么也不干
如果树结果了，吃苹果的人要去吃，否则什么也不干
被观察者：
1 将观察者放入自己的观察者列表中，registerObserver(self, observer)
2 当被观察者状态发生时，notify Observer(self)，此方法可能不止一个
3 当观察者众多，而notify仅针对某一部分观察者时，要有筛选观察者的removeObserver(self, observer)
观察者：
1 当被通知后，自己应该做些什么update(self, )
2 是否对被观察者状态做改变？
"""
# 观察者的接口，状态改变，还有一些其他的事
class Observer:
    def update(self, stat):
        return
    def display(self):
        return
# 被观察者
class Observed:
    def registerObserver(self, observer):
        return
    def removeObserver(self, observer):
        return
    def noticyObservers(self):
        return
# 具体实现被观察者植物类
class plant(Observed):
    def __init__(self):
        # 这个地方先虚写观察者和状态
        self.observers = []
        self.stat = 'new'
        return

    def registerObserver(self, observer):
        self.observers.append(observer)
        return
    def removeObserver(self, observer):
        self.observers.remove(observer)
        return
    def noticyObservers(self):
        for item in self.observers:
            # 观察者收到当前状态，然后update一下
            item.update(self.stat)
        return
    # 状态改变之后，通知Observer
    def statusChanged(self):
        self.noticyObservers()
    def setStatus(self, status):
        self.stat = status
        self.statusChanged()

# 观察者
class planter(Observer):
    def __init__(self, plant):
        self.plant = plant
        self.doing = 'nothing'
        plant.registerObserver(self)
        return
    def update(self, stat):
         if stat == 'ill':
             self.doing = 'work'
         else:
             self.doing = 'nothing'
         self.display()
         return
    def display(self):
        print("I am planter,my plant now is %s, i doing %s." %
              (self.plant.stat, self.doing))

class eater(Observer):
    def __init__(self, plant):
        self.plant = plant
        self.doing = 'nothing'
        plant.registerObserver(self)
    def update(self, stat):
        if stat == 'ok':
            self.doing = 'eating'
        else:
            self.doing = 'nothing'
        self.display()
    def display(self):
        print("I am eater,my plant now is %s, i doing %s." %
              (self.plant.stat, self.doing))
if __name__ =='__main__':
    tree = plant()
    display1 = planter(tree)
    display2 = eater(tree)
    tree.setStatus('ill')
    tree.setStatus('ok')

