from ovad.commons import ArgumentsDispatcher, OvadMeta

class SomeClass(metaclass=OvadMeta):

    def foo(self):
        pass

    def foo(self, a, b):
        pass

    def bar(self):
        pass

    def bar(self, a, b):
        pass

def test_commons():
    a = SomeClass()