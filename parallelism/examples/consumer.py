def coroutine():
    for i in range(1, 6):
        print("From generator {}".format((yield i)))


c = coroutine()

c.send(None)

try:
    while True:
        print("From user {}".format(c.send(1)))
except StopIteration:
    pass
