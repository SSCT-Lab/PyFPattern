

def __new__(cls, name, abbrev=None, dimension=None, scale_factor=None, **assumptions):
    if (not isinstance(name, Symbol)):
        name = Symbol(name)
    if (dimension is not None):
        SymPyDeprecationWarning(deprecated_since_version='1.3', issue=14319, feature='Quantity arguments', useinstead='SI_quantity_dimension_map').warn()
    if (scale_factor is not None):
        SymPyDeprecationWarning(deprecated_since_version='1.3', issue=14319, feature='Quantity arguments', useinstead='SI_quantity_scale_factors').warn()
    if (abbrev is None):
        abbrev = name
    elif isinstance(abbrev, string_types):
        abbrev = Symbol(abbrev)
    obj = AtomicExpr.__new__(cls, name, abbrev)
    obj._name = name
    obj._abbrev = abbrev
    if (dimension is not None):
        obj.set_dimension(dimension)
    if (scale_factor is not None):
        obj.set_scale_factor(scale_factor)
    return obj
