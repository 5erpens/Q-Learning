# Decorator
class Singleton(object):

    def __init__(self, cls):
        self.cls = cls
        self.instance = {}

    def __call__(self, *args, **kwargs):
        if self.cls not in self.instance:
            self.instance[self.cls] = self.cls(*args, **kwargs)
        return self.instance[self.cls]


# Super Singleton class works in Python 2 & 3
class _singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class singleton(_singleton('SingletonMeta', (object,), {})):

    def class_type(self):
        return self.__class__.__name__

    def instance_id(self):
        return hex(id(self))

    def class_instance(self):
        return str(self.class_type()) + " object at " + str(self.instance_id().upper())

    pass
