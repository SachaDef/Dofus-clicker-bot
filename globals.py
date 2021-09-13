import queue as q

class MyQueue(q.Queue):
    def __init__(self):
        super().__init__(maxsize=1)
        self.running = True
        self.open = True
    def MyPut(self, item):
        if self.open:
            try:
                super().put_nowait(item)
            except q.Full:
                pass
    def MyGet(self):
        try:
            return super().get_nowait()
        except q.Empty:
            pass

global popQ
popQ = MyQueue()