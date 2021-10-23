def _Quantity_constructor_postprocessor_Add(expr):
    deset = {tuple(sorted(Dimension(Quantity.get_dimensional_expr(i)).get_dimensional_dependencies().items())) for i in expr.args if ((i.free_symbols == set()) and (not i.is_number))}
    if (len(deset) > 1):
        raise ValueError('summation of quantities of incompatible dimensions')
    return expr