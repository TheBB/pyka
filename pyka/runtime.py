import ctypes as ct
import inspect

from pyka.ast import prototype


__all__ = [
    'put',
]


class Wrap:

    def __init__(self, callback):
        self.args = inspect.getfullargspec(callback).args
        args = [ct.c_double] * (len(self.args) + 1)
        type_ = ct.CFUNCTYPE(*args)

        self.callback = callback
        self.c_callback = type_(callback)

    def __str__(self):
        return self.callback.__name__

    @property
    def addr(self):
        return ct.cast(self.c_callback, ct.c_void_p).value

    @property
    def prototype(self):
        return prototype(self.callback.__name__, *self.args)


def put(a):
    print(a)
    return 0.0
