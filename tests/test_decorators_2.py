
def deco_p(p1=1, p2=2):
    def wrapper(cls):
        print(f'running wrapper {cls=} {p1=} {p2=}')
        return cls

    print(f'about to return wrapper {p1=} {p2=}')
    return wrapper

class TestDeco2:
    def test_deco_wrapper(self):
        @deco_p(10, 20)
        class Ignore:
            pass

        assert True
