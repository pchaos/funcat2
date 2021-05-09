# -*- coding: utf-8 -*-
from py_singleton import singleton


@singleton
class FuncCounter(object):
    """Limitation For best performance, the code to create instance is not thread-safe, however, after the instance is created it should be safe for multi-threading.
    It is recommended to call instance() once during the initial phrase of your app in a single thread.
    """

    def __init__(self):
        FuncCounter.count = {}

    def update(self, value):
        self.count[value] = self.count.get(value) + 1 if self.count.get(value, 0) > 0 else 1

    def get(self, value):
        return self.count[value]


if __name__ == '__main__':
    a0 = FuncCounter.instance()
    a1 = FuncCounter()
    a2 = FuncCounter()
    a3 = FuncCounter.instance()

    for i in range(10):
        FuncCounter.instance().update("a")
    assert FuncCounter.count["a"] == 10
    print(FuncCounter.count)
    print(FuncCounter.instance().get("a"))
    assert a1 is a2
    assert a1 is a3
