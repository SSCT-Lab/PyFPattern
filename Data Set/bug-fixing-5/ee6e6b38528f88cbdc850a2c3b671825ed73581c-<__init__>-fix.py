def __init__(self, class_instance, methodtype='method'):
    types = {'method', 'classmethod', 'staticmethod', 'property'}
    if (methodtype not in types):
        raise ValueError(f'methodtype must be one of {methodtype}, got {types} instead.')
    self.methodtype = methodtype
    self.class_instance = class_instance