import pytest


class TestDescriptors:
    def test_default_values(self):
        class DefaultValues:
            value1 = 5
            value2 = 71

        dv = DefaultValues()
        assert dv.value1 == 5
        assert dv.value2 == 71
        assert 'value1' not in dv.__dict__
        assert 'value2' not in dv.__dict__
        dv.value1 = 6
        assert dv.value1 == 6
        assert dv.value2 == 71
        assert 'value1' in dv.__dict__
        assert 'value2' not in dv.__dict__

    def test_realpython_idea(self):
        class EvenNumber:
            def __set_name__(self, owner, name):
                self.name = name

            def __get__(self, instance, type=None):
                print(f'{type=}')
                return instance.__dict__.get(self.name) or 0

            def __set__(self, instance, value):
                instance.__dict__[self.name] = \
                    (value if value % 2 == 0 else 0)

        class OnlyEvens:
            value1 = EvenNumber()
            value2 = EvenNumber()

        oe = OnlyEvens()
        oe.value1 = 4
        oe.value2 = 3
        assert oe.value1 == 4
        assert oe.value2 == 0

    def test_forwarding(self):
        needy = NeedsInfo()
        assert needy.info == "info from InfoHolder"

    def test_cannot_store(self):
        needy = NeedsInfo()
        with pytest.raises(AttributeError) as error:
            needy.info = "cannot do this"
        assert str(error.value) == "cannot set 'info'"

class Forwarder:
    def __init__(self, receiver_name):
        self.receiver_name = receiver_name

    def __set_name__(self, owner, attribute_name):
        self.attribute_name = attribute_name

    def __get__(self, instance, type=None):
        receiver = getattr(instance, self.receiver_name)
        return getattr(receiver, self.attribute_name)

    def __set__(self, instance, value):
        raise AttributeError(f"cannot set '{self.attribute_name}'")

class InfoHolder:
    def __init__(self):
        self.info = "info from InfoHolder"

class NeedsInfo:
    info = Forwarder('extra_data')

    def __init__(self):
        self.extra_data = InfoHolder()


