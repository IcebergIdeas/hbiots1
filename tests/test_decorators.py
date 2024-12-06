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


def deco3(cls):
    setattr(cls, '__getattr__',open_getattr)
    return cls

def open_getattr(self, key):
    if key == 'fargle':
        return lambda: 666
    else:
        return super(self.__class__, self).__getattribute__( key)


@deco3
class Deco3:
    pass


class TestDecorators:
    def test_deco1_class(self):
        d1 = Deco1()
        assert d1.bar() == 42
        assert d1.mumble() == "mumbling"

    def test_deco2_class(self):
        d2 = Deco2()
        assert d2.foo() == 42
        assert d2.fargle() == 666

    # @pytest.mark.xfail
    # # see test_decorators_2.
    # # parens mean that you have to define and return a wrapper
    # def test_deco2_with_parens(self):
    #     @deco2()
    #     class NoMatter:
    #         pass
    #     assert NoMatter().fargle() == 666
    #
    # @pytest.mark.xfail
    # def test_not_a_class_method(self):
    #     d3 = Deco3()
    #     # I don't understand why this doesn't work
    #     assert d3.fargle == 666
