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
