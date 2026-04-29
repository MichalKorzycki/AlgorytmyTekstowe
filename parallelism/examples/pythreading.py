from threading import Thread
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
    setproctitle.setproctitle(f'threading-f({name})')
    sleep(10)

    print('hello', name)


if __name__ == '__main__':
    info('main line')
    setproctitle.setproctitle(f'threading-main')
    p1 = Thread(target=f, args=('bob',))
    p2 = Thread(target=f, args=('alice',))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
