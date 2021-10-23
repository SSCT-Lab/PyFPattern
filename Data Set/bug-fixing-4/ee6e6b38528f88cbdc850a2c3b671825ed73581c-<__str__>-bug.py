def __str__(self) -> str:
    if (self.methodtype == 'classmethod'):
        name = self.class_instance.__name__
    else:
        name = type(self.class_instance).__name__
    msg = f'This {self.methodtype} must be defined in the concrete class {name}'
    return msg.format(methodtype=self.methodtype, name=name)