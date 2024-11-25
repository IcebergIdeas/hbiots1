
class deco_class_1:
    def __init__(self, thing):
        self.thing = thing

    def __call__(self):
        return self.thing()

class deco_class_parm:
    def __init__(self, param):
        self.param = param

    def __call__(self, callable):
        class decorated(callable):
            def __init__(self, *args, **kwargs):
                super().__init__(self)

            def bar(self):
                return 'mumble'

        return decorated

class TestDecoratorClasses:
    def test_first_example(self):
        @deco_class_1
        class Decorated:
            def __init__(self):
                self.foo = 42

        d = Decorated()
        assert d.foo == 42

    def test_parameterized_decorator(self):
        @deco_class_parm(37)
        class Decorated:
            def __init__(self, unexpected):
                self.foo = 42

        d = Decorated()
        assert d.foo == 42
        assert d.bar() == "mumble"

# class DecoratorWithArguments:
#     def __init__(self, arg1, arg2):
#         self.arg1 = arg1
#         self.arg2 = arg2
#
#     def __call__(self, func):
#         def wrapper(*args, **kwargs):
#             print(f"Decorator arguments: {self.arg1}, {self.arg2}")
#             print("Before function call")
#             result = func(*args, **kwargs)
#             print("After function call")
#             return result
#         return wrapper
#
# @DecoratorWithArguments("Hello", "World")
# def my_function(a, b):
#     print(f"Inside my_function with {a}, {b}")
#     return a + b
#
# result = my_function(1, 2)
# print("Result:", result)

