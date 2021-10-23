

def cse(exprs, symbols=None, optimizations=None, postprocess=None, order='canonical', ignore=()):
    ' Perform common subexpression elimination on an expression.\n\n    Parameters\n    ==========\n\n    exprs : list of sympy expressions, or a single sympy expression\n        The expressions to reduce.\n    symbols : infinite iterator yielding unique Symbols\n        The symbols used to label the common subexpressions which are pulled\n        out. The ``numbered_symbols`` generator is useful. The default is a\n        stream of symbols of the form "x0", "x1", etc. This must be an\n        infinite iterator.\n    optimizations : list of (callable, callable) pairs\n        The (preprocessor, postprocessor) pairs of external optimization\n        functions. Optionally \'basic\' can be passed for a set of predefined\n        basic optimizations. Such \'basic\' optimizations were used by default\n        in old implementation, however they can be really slow on larger\n        expressions. Now, no pre or post optimizations are made by default.\n    postprocess : a function which accepts the two return values of cse and\n        returns the desired form of output from cse, e.g. if you want the\n        replacements reversed the function might be the following lambda:\n        lambda r, e: return reversed(r), e\n    order : string, \'none\' or \'canonical\'\n        The order by which Mul and Add arguments are processed. If set to\n        \'canonical\', arguments will be canonically ordered. If set to \'none\',\n        ordering will be faster but dependent on expressions hashes, thus\n        machine dependent and variable. For large expressions where speed is a\n        concern, use the setting order=\'none\'.\n    ignore : iterable of Symbols\n        Substitutions containing any Symbol from ``ignore`` will be ignored.\n\n    Returns\n    =======\n\n    replacements : list of (Symbol, expression) pairs\n        All of the common subexpressions that were replaced. Subexpressions\n        earlier in this list might show up in subexpressions later in this\n        list.\n    reduced_exprs : list of sympy expressions\n        The reduced expressions with all of the replacements above.\n\n    Examples\n    ========\n\n    >>> from sympy import cse, SparseMatrix\n    >>> from sympy.abc import x, y, z, w\n    >>> cse(((w + x + y + z)*(w + y + z))/(w + x)**3)\n    ([(x0, y + z), (x1, w + x)], [(w + x0)*(x0 + x1)/x1**3])\n\n    Note that currently, y + z will not get substituted if -y - z is used.\n\n     >>> cse(((w + x + y + z)*(w - y - z))/(w + x)**3)\n     ([(x0, w + x)], [(w - y - z)*(x0 + y + z)/x0**3])\n\n    List of expressions with recursive substitutions:\n\n    >>> m = SparseMatrix([x + y, x + y + z])\n    >>> cse([(x+y)**2, x + y + z, y + z, x + z + y, m])\n    ([(x0, x + y), (x1, x0 + z)], [x0**2, x1, y + z, x1, Matrix([\n    [x0],\n    [x1]])])\n\n    Note: the type and mutability of input matrices is retained.\n\n    >>> isinstance(_[1][-1], SparseMatrix)\n    True\n\n    The user may disallow substitutions containing certain symbols:\n    >>> cse([y**2*(x + 1), 3*y**2*(x + 1)], ignore=(y,))\n    ([(x0, x + 1)], [x0*y**2, 3*x0*y**2])\n\n    '
    from sympy.matrices import MatrixBase, Matrix, ImmutableMatrix, SparseMatrix, ImmutableSparseMatrix
    if isinstance(exprs, (Basic, MatrixBase)):
        exprs = [exprs]
    copy = exprs
    temp = []
    for e in exprs:
        if isinstance(e, (Matrix, ImmutableMatrix)):
            temp.append(Tuple(*e._mat))
        elif isinstance(e, (SparseMatrix, ImmutableSparseMatrix)):
            temp.append(Tuple(*e._smat.items()))
        else:
            temp.append(e)
    exprs = temp
    del temp
    if (optimizations is None):
        optimizations = list()
    elif (optimizations == 'basic'):
        optimizations = basic_optimizations
    reduced_exprs = [preprocess_for_cse(e, optimizations) for e in exprs]
    if (symbols is None):
        symbols = numbered_symbols(cls=Symbol)
    else:
        symbols = iter(symbols)
    opt_subs = opt_cse(reduced_exprs, order)
    (replacements, reduced_exprs) = tree_cse(reduced_exprs, symbols, opt_subs, order, ignore)
    exprs = copy
    for (i, (sym, subtree)) in enumerate(replacements):
        subtree = postprocess_for_cse(subtree, optimizations)
        replacements[i] = (sym, subtree)
    reduced_exprs = [postprocess_for_cse(e, optimizations) for e in reduced_exprs]
    for (i, e) in enumerate(exprs):
        if isinstance(e, (Matrix, ImmutableMatrix)):
            reduced_exprs[i] = Matrix(e.rows, e.cols, reduced_exprs[i])
            if isinstance(e, ImmutableMatrix):
                reduced_exprs[i] = reduced_exprs[i].as_immutable()
        elif isinstance(e, (SparseMatrix, ImmutableSparseMatrix)):
            m = SparseMatrix(e.rows, e.cols, {
                
            })
            for (k, v) in reduced_exprs[i]:
                m[k] = v
            if isinstance(e, ImmutableSparseMatrix):
                m = m.as_immutable()
            reduced_exprs[i] = m
    if (postprocess is None):
        return (replacements, reduced_exprs)
    return postprocess(replacements, reduced_exprs)
