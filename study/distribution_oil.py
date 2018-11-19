# -*- coding: utf-8 -*-
# author: WangYun 
# time :2018/10/24 

from collections import deque
# 输入当前状态，装油的量
def nextstep(current_state, oil_volume):
    next_action = [
        (from_, to_)
        for from_ in range(3) for to_ in range(3)
        if from_ != to_ and current_state[from_] > 0 and
           current_state[to_] < oil_volume[to_]

    ]
    for from_, to_ in next_action:
        next_state = list(current_state)
        if current_state[from_] + current_state[to_] > oil_volume[to_]:
            next_state[from_] -= (oil_volume[to_] - current_state[to_])
            next_state[to_] = oil_volume[to_]
        else:
            next_state[from_] = 0
            next_state[to_] = current_state[to_] + current_state[from_]
        yield next_state

def seachresult(record, oil_volume = [10, 7, 3], final_state=[5, 5, 0]):
    global num, record_list
    current_state = record[-1]
    next_stage = nextstep(current_state, oil_volume)

    for stage in next_stage:
        if stage not in record:
            record.append(stage)
            if stage == final_state:
                numm = num + 1
                s_numm = str(numm)
                str_record = ''
                for i in record:
                    str_record += str(i)
                    if i != [5, 5, 0]:
                        str_record += '->'
                print("方法 {0}:{1}".format(s_numm, str_record))
                record_list.append(deque(record))
                num += 1
            else:
                seachresult(record, oil_volume, final_state)
            record.pop()




def main():
    pass


if __name__ == '__main__':
    initial_oil_state = [10, 0, 0]
    oil_volume = [10, 7, 3]
    num = 0
    record_list = []
    record = deque()
    record.append(initial_oil_state)
    seachresult(record)
    number = "广度优先搜索共有 {0} 种方法".format(num)
    shortest = "路径最短的方法中操作步总数为 {0} ".format(min([len(i) for i in record_list]))

    print(number)
    print(shortest)