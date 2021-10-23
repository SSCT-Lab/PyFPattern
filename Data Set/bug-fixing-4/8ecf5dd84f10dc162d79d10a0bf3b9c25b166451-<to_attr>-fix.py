@staticmethod
def to_attr(arg):
    "\n        Create ParamAttr[s].\n\n        Args:\n            arg: Arguments to initialize ParamAttr[s]. arg's type can be\n                str, Initializer, float, WeightDecayRegularizer, BaseGradientClipAttr,\n                bool, ParamAttr, or a list of above type.\n\n        Returns:\n            ParamAttr[s]: ParamAttr[s] initialized with arg.\n\n        Raises:\n            arg can not initialize a ParamAttr.\n        "
    if (arg is None):
        return ParamAttr()
    elif (isinstance(arg, list) or isinstance(arg, tuple)):
        return [ParamAttr.to_attr(a) for a in arg]
    elif isinstance(arg, ParamAttr):
        return arg
    elif (isinstance(arg, str) or isinstance(arg, unicode)):
        return ParamAttr(name=arg)
    elif isinstance(arg, Initializer):
        return ParamAttr(initializer=arg)
    elif isinstance(arg, WeightDecayRegularizer):
        return ParamAttr(regularizer=arg)
    elif isinstance(arg, bool):
        return (ParamAttr.to_attr(None) if arg else False)
    else:
        raise TypeError('{0} cast to ParamAttr'.format(type(arg)))