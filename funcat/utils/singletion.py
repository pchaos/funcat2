# -*- coding: utf-8 -*-
from py_singleton import singleton


@singleton
class FuncCounter(object):
    """单例模式计数器
    Limitation For best performance, the code to create instance is not thread-safe, however, after the instance is created it should be safe for multi-threading.
    It is recommended to call instance() once during the initial phrase of your app in a single thread.
    FuncCounter.counter记录记数情况
    """

    def __init__(self):
        FuncCounter.counter = {}

    def update(self, value):
        self.counter[value] = self.counter.get(value) + 1 if self.counter.get(value, 0) > 0 else 1

    def get(self, value):
        return self.counter[value]

    def __str__(self):
        # return object.__str__(self, *args, **kwargs)
        return f"Counter:{self.counter}"
    
    def __repr__(self):
        return f"Counter:{self.counter}; length:{len(self.counter)}"

if __name__ == '__main__':
    a0 = FuncCounter.instance()
    a1 = FuncCounter()
    a2 = FuncCounter()
    a3 = FuncCounter.instance()

    for i in range(10):
        FuncCounter.instance().update("a")
    assert FuncCounter.counter["a"] == 10
    print(FuncCounter.counter)
    print(FuncCounter.instance().get("a"))
    assert a1 is a2
    assert a1 is a3
    print(FuncCounter)