
def deco1(cls):
    setattr(cls, 'mumble', my_mumble)
    return cls

def my_mumble(self):
    return "mumbling"

@deco1
class Deco1:
    def __init__(self):
        self.foo = 42

    def bar(self):
        return self.foo


def deco2(cls):
    setattr(cls, '__getattr__',deco2_fake.my_getattr)
    return cls

class deco2_fake:
    def my_getattr(self, key):
        if key == 'fargle':
            return lambda: 666
        else:
            return super(self.__class__, self).__getattribute__( key)

@deco2
class Deco2:
    def foo(self):
        return 42




class TestDecorators:
    def test_deco1_class(self):
        d1 = Deco1()
        print(dir(d1))
        assert d1.bar() == 42
        assert d1.mumble() == "mumbling"

    def test_deco2_class(self):
        d2 = Deco2()
        assert d2.foo() == 42
        assert d2.fargle() == 666