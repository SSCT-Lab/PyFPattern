

@classmethod
def construct_from_string(cls, string):
    if (string == cls.name):
        return cls()
    else:
        raise TypeError("Cannot construct a '{}' from '{}'".format(cls, string))
