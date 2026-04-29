from multiprocessing import Process
import os
from time import sleep
import setproctitle


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def f(name):
    info('> function f')
    setproctitle.setproctitle(f'multiprocessing-f({name})')
    sleep(10)

    print('hello', name)


if __name__ == '__main__':
    info('main line')
    setproctitle.setproctitle(f'multiprocessing-main')
    p1 = Process(target=f, args=('bob',))
    p2 = Process(target=f, args=('alice',))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
