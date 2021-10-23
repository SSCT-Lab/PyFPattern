def is_compatible_with(x, Type):
    '                                                                                                                                                                                                \n    Check if x has a type compatible with Type                                                                                                                                                         \n    :param x: object to be checked                                                                                                                                                                     \n    :param Type: target type to check x over                                                                                                                                                           \n    \n    '
    if (type(x) == Type):
        return True
    try:
        if ((float == Type) or (int == Type)):
            if ((not isinstance(x, str)) and (not isinstance(x, bool))):
                return convert_and_compare(x, Type)
        elif (bool == Type):
            if (not isinstance(x, str)):
                return convert_and_compare(x, Type)
        else:
            return False
    except:
        return False