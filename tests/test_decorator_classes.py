
class deco_class_1:
    def __init__(self, thing):
        print(f'decorator init {thing}')
        self.thing = thing

    def __call__(self):
        print(f'call {self.thing.__name__}')
        return self.thing()

class deco_class_parm:
    def __init__(self, param):
        print(f'decorator init {param}')
        self.param = param

    def __call__(self, callable):
        class decorated(callable):
            def __init__(self, *args, **kwargs):
                print(f'decorated init {self} {args}')
                super().__init__(self)

            def bar(self):
                return 'mumble'

        print(f'call {callable.__name__}')
        return decorated

class TestDecoratorClasses:
    def test_first_example(self):
        @deco_class_1
        class Decorated:
            def __init__(self):
                print(f'Decorated init {self}')
                self.foo = 42

        print('create')
        d = Decorated()
        print('created')
        assert d.foo == 42

    def test_parameterized_decorator(self):
        @deco_class_parm(37)
        class Decorated:
            def __init__(self, unexpected):
                print(f'Decorated init {self}\n{unexpected=}')
                self.foo = 42

        print("create")
        d = Decorated()
        print("created")
        assert d.foo == 42
        assert d.bar() == "mumble"
