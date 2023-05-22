import functools


def event(func):
    def modified(obj, *arg, **kw):
        func(obj, *arg, **kw)
        obj._Observable__fire_callbacks(func.__name__, *arg, **kw)

    functools.update_wrapper(modified, func)
    return modified


class Observable(object):
    def __init__(self):
        self.__observers = {}

    def add_observer(self, method_name, observer):
        s = self.__observers.setdefault(method_name, set())
        s.add(observer)

    def __fire_callbacks(self, method_name, *arg, **kw):
        if method_name in self.__observers:
            for o in self.__observers[method_name]:
                o(*arg, **kw)
