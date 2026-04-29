# https://stackoverflow.com/questions/9968592/turn-functions-with-a-callback-into-python-generators/36946209#36946209

from contextlib import closing
from itertools import count

processed = []


class FakeFtp(object):
    def __init__(self):
        self.data = iter(["aaa", "bbb", "ccc", "ddd"])

    def login(self, user, password):
        self.user = user
        self.password = password

    def retrbinary(self, cmd, call_back):
        for chunk in self.data:
            call_back(chunk)


def process_chunks():
    for i in count():
        try:
            # (repeatedly) get the chunk to process
            chunk = yield
        except GeneratorExit:
            # finish_up
            print("Finishing up.")
            return
        else:
            # Here process the chunk as you like
            print("inside coroutine, processing chunk:", i, chunk)
            product = "processed({i}): {chunk}".format(i=i, chunk=chunk)
            processed.append(product)


with closing(process_chunks()) as coroutine:
    # Get the coroutine to the first yield
    coroutine.__next__()
    ftp = FakeFtp()
    # next line repeatedly calls `coroutine.send(data)`
    ftp.retrbinary("RETR binary", call_back=coroutine.send)
    # each callback "jumps" to `yield` line in `process_chunks`

print("processed result", processed)
print("DONE")