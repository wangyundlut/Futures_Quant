# -*- coding: utf-8 -*-

"""
class threading.Thread(
group=None, 保留变量 以后扩展用的 暂时不用考虑
target=None, 通过run来运行目标函数 默认None
name=None, 名字
args=(), 元组参数 target调用
 kwargs={}, *, 参数的字典 target所调用
 daemon=None)


这个构造函数通常会用一些关键字参数，下面我们了解下这些关键字：
group ：这个变量作为保留变量，是为了以后扩展用的，暂时可以不用考虑。
target: 是通过run()
方法调用的可调用对象。默认为无，这意味着什么都不做。
name：线程的名字。默认情况下，一个唯一的名称是”thread - n”，的形式，其中n是一个小的十进制数。
args：元组参数，为target所调用的。
kwargs：关键字参数的字典，为target所调用的。
daemon: 设置daemon是否daemon
如果没有显示设置，daemon的属性时从当前线程继承。
如果子类重写此构造函数，它必须确保在做别的事情之前调用基类的构造函数（thread.__init__()。

1,threading.active_aount()
这个函数返回当前线程的个数，这个程序的值也等于 列表enumerate()
的长度。
2.threading.current_thread()
返回当前的线程对象。如果调用的线程不是通过threading 这个模块创建的，那么返回的是一个有限功能的dummy thread objects'(哑线程对象。
3.threading.get_ident()
返回当先线程的索引，这个索引是一个非零的整数。
4.threading.enumereate()
返回当前运行线程的列表。这个列表包含dummy thread objects'(哑线程对象，daemon thread'(守护线程)，和那些主线程。这些线程的状态可能时已经运行的，还没有运行的。
5.threading.main_thread()
返回主线程，正常情况下，主线程就是python 解释器运行时开始的那个线程。
6,threading.settrace(func)
当开始调用threading 模块的时候设定 跟踪函数(trace function )，
7,threading.setpeofile()
 设定 profile function

8,threading.stack_size(【size】)
返回创建新线程时线程堆的大小。

class threading.Sempaphore(value = 1) --限制资源的并发访问。
   semaphore 是一个内部的计数器，它会随着acquire()的请求减小，也会随着release()的释放增加。这个计数器的值不会小于零，当acquier() 发现计数器的值为0时，那么当前对象会等待直到其他对象release()为止。
acquier(blocking = True ,timeout = None)
release()

class threading.Timer(interval,function,args = None ,kwargs = None)
    创建一个时间对象，设定一个函数于多长时间后运行。
   Timer.start()
   Timer.cancel()
——————
class.threading.Barrier(parties,action = None ,timeout = None)
   wait(timeout = None)
    这个类对那些固定数量的，需要相互等待的线程。提供了一个简单的同步机制。
    reset()
    abort()
    parties
    n_waiting
    broken


 primitive lock 有两种状态 unlock 和 lock，它有两种基本的方法，acpuire()和release()，当状态为unllocked时，调用acquire()方法会将状态改变为locked ，并立刻得到返回。当状态为locked时，acquire()方法直到另一个线程调用release()方法将状态改为unlocked，此时才会将状态设为locked并返回。而realease()方法只会被locked状态所调用， 他会将转台改为unlocked()并且立刻返回。将realease作用unlocked的lock时，将会抛出Runtimerror .

 两个方法 ：
        acquier(blocking = True,timeout = -1)
        release()

#lock = threading.Lock()
#lock.acquire()
#locke.release()

守护线程和非守护线程：
守护线程可以一直运行而不阻塞主程序推出。如果一个服务器无法用一种容易的方法来中断线程，
或者希望线程工作到一半时终止而不损失或者破坏数据，对于这些服务使用守护线程就很有用。
要设置一个守护线程可以用setDaemin()，并提供参数True。

要等待一个守护线程完成工作，需要使用join（）方法。


join([timeout])方法：阻塞当前线程，直到调用join方法的线程中断后，才会继续当前线程。
is_alive()方法：判断线程是否在运行。
setDaemon(True)方法:设置线程为守护线程，该方法必须在start()前调用。
一个线程为守护线程，则当主线程运行完毕后，若守护线程没有运行完毕则会随主线程一起退出。
而对于非守护线程，主线程运行完毕后会等待非守护线程结束然后一起退出。

当代码执行到show_filename中的return "filename: %s" % filename语句时，
解析器按照下面的顺序查找filename变量：
Local - 本地函数(show_filename)内部，通过任何方式赋值的，而且没有被global关键字声明为全局变量的filename变量；
Enclosing - 直接外围空间(上层函数wrapper)的本地作用域，查找filename变量(如果有多层嵌套，则由内而外逐层查找，直至最外层的函数)；
Global - 全局空间(模块enclosed.py)，在模块顶层赋值的filename变量；
Builtin - 内置模块(__builtin__)中预定义的变量名中查找filename变量；
在任何一层先找到了符合要求的filename变量，则不再向更外层查找。
如果直到Builtin层仍然没有找到符合要求的变量，则抛出NameError异常。这就是变量名解析的：LEGB法则。

"""


import threading
import time
import random
import queue


def producer():
    print("chef: 等人买包子")
    event.wait()
    event.clear()
    print("开始做包子")
    time.sleep(10)
    print("包子好了")
    event.set()

def consumer():
    print("我去买包子")
    event.set()
    time.sleep(2)
    print("等着包子做好")
    event.wait()
    print("thanks")

def time_seconds(sec, dic):
    print('timesleep ' + str(sec['秒']) +' seconds' + dic['s'])
    time.sleep(sec['秒'])

    print('timesleep Done')

if __name__=='__main__':
    # 测试
    event = threading.Event()
    sec = {}
    d = {}
    sec['秒'] = 5
    d['s'] = 'f'
    c1 = threading.Thread(target=time_seconds, args=(sec,d,))
    sec2 = {}
    d2 = {}
    sec2['秒'] = 10
    d2['s'] = 'k'
    c2 = threading.Thread(target=time_seconds, args=(sec2,d2,))
    c2.start()
    c1.start()
    c1.join()
    c2.join()
    print('Done')

