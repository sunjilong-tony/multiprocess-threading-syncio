#! /usr/bin/python3
# coding= utf-8
import random, os, time
from multiprocessing import Process, Lock   # 引入Lock模块

def work(n, lock):
    lock.acquire()  # 加锁,保证每次只有一个进程在执行锁内的程序.此时对于所有加锁的进程来说,都变成了串行.
    print("{} >>> {}号进程正在执行".format(n, os.getpid()))
    time.sleep(random.random())
    print("{} >>> {}号进程执行完毕".format(n, os.getpid()))
    lock.release()  # 解锁,解锁之后其他进程才能执行自己的程序

if __name__ == '__main__':
    lock = Lock()   # 创建Lock对象
    for i in range(5):
        p = Process(target=work, args=(i, lock))
        p.start()

# 执行结果
# 0 >>> 8056号进程正在执行
# 0 >>> 8056号进程执行完毕
# 1 >>> 3096号进程正在执行
# 1 >>> 3096号进程执行完毕
# 2 >>> 268号进程正在执行
# 2 >>> 268号进程执行完毕
# 3 >>> 8948号进程正在执行
# 3 >>> 8948号进程执行完毕
# 4 >>> 10612号进程正在执行
# 4 >>> 10612号进程执行完毕

# 得出结论: 加锁后程序由并发变成了串行,牺牲了运行效率,但避免了竞争,种情况虽然使用加锁的形式实现了顺序的执行,但是程序又重新变成串行了. 这种做法浪费了时间却保证了数据的安全.

##加锁可以保证:多个进程修改同一块数据时,同一时间只能有一个任务可以进行修改,即串行的修改.这种方式虽然牺牲了速度(效率)却保证了数据安全.

# 虽然可以用文件共享数据实现进程间通信，但问题是：
# 1.效率低（共享数据基于文件，而文件是硬盘上的数据）
# 2.需要自己加锁处理
#
# #因此我们最好找寻一种解决方案能够兼顾：1、效率高（多个进程共享一块内存的数据）2、帮我们处理好锁问题。这就是mutiprocessing模块为我们提供的基于消息的IPC通信机制: 队列和管道.
#
# 队列和管道都是将数据存放于内存中
#
# 队列又是基于（管道+锁）实现的，可以让我们从复杂的锁问题中解脱出来,我们应该尽量避免使用共享数据,尽可能使用消息传递和队列,避免处理复杂的同步和锁问题,而且在进程数目增多时,往往可以获得更好的可获展性.
#
# 进程锁总结
