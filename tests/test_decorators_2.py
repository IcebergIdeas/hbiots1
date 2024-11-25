
def deco_p(p1=1, p2=2):
    def wrapper(cls):
        return cls

    return wrapper

class TestDeco2:
    def test_deco_wrapper(self):
        @deco_p(10, 20)
        class Ignore:
            pass

        assert True
