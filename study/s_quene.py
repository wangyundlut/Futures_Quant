"""
创建一个“队列”对象

import queue
myqueue = Queue.Queue(maxsize = 10)
Queue.Queue类即是一个队列的同步实现。maxsize 队列的长度

myqueue.put(10) 将一个值放入队列中
put()有两个参数，第一个item为必需的，为插入项目的值
1 ？？？ 这个值指的是什么？num str class  dict?
第二个block为可选参数，默认为1
如果队列当前为空且block为1，put()方法就使调用线程暂停,直到空出一个数据单元。
如果block为0，put方法将引发Full异常。
将一个值从队列中取出
myqueue.get()
调用队列对象的get()方法从队头删除并返回一个项目。可选参数为block，默认为True。
如果队列为空且block为True，get()就使调用线程暂停，直至有项目可用。
如果队列为空且block为False，队列将引发Empty异常。
2 ?????block看起来是类似一个flag的作用 值为空且block=true是一个 一个线程是否继续的控制

python queue模块有三种队列:
1、python queue模块的FIFO队列先进先出。Queue.Queue(maxsize) FIFO
2、LIFO类似于堆。即先进后出。 Queue.LifoQueue(maxsize) LIFO
3、还有一种是优先级队列级别越低越先出来。 Queue.PriorityQueue(maxsize) 优先级队列

Queue.qsize() 返回队列的大小 里面有几个
Queue.empty() 如果队列为空，返回True,反之False
Queue.full() 如果队列满了，返回True,反之False
Queue.full 与 maxsize 大小对应
Queue.get(block = True, timeout = 1)获取队列，timeout等待时间
Queue.get_nowait() 相当Queue.get(False)
Queue.put(item，timeout) 写入队列，timeout等待时间
Queue.put_nowait(item) 相当Queue.put(item, False)
Queue.task_done() 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号
Queue.join() 实际上意味着等到队列为空，再执行别的操作




"""