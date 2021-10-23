

def einsum(*operands, **kwargs):
    "\n    einsum(subscripts, *operands, out=None, dtype=None, order='K',\n           casting='safe', optimize=False)\n\n    Evaluates the Einstein summation convention on the operands.\n\n    Using the Einstein summation convention, many common multi-dimensional\n    array operations can be represented in a simple fashion.  This function\n    provides a way to compute such summations. The best way to understand this\n    function is to try the examples below, which show how many common NumPy\n    functions can be implemented as calls to `einsum`.\n\n    Parameters\n    ----------\n    subscripts : str\n        Specifies the subscripts for summation.\n    operands : list of array_like\n        These are the arrays for the operation.\n    out : {ndarray, None}, optional\n        If provided, the calculation is done into this array.\n    dtype : {data-type, None}, optional\n        If provided, forces the calculation to use the data type specified.\n        Note that you may have to also give a more liberal `casting`\n        parameter to allow the conversions. Default is None.\n    order : {'C', 'F', 'A', 'K'}, optional\n        Controls the memory layout of the output. 'C' means it should\n        be C contiguous. 'F' means it should be Fortran contiguous,\n        'A' means it should be 'F' if the inputs are all 'F', 'C' otherwise.\n        'K' means it should be as close to the layout as the inputs as\n        is possible, including arbitrarily permuted axes.\n        Default is 'K'.\n    casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional\n        Controls what kind of data casting may occur.  Setting this to\n        'unsafe' is not recommended, as it can adversely affect accumulations.\n\n          * 'no' means the data types should not be cast at all.\n          * 'equiv' means only byte-order changes are allowed.\n          * 'safe' means only casts which can preserve values are allowed.\n          * 'same_kind' means only safe casts or casts within a kind,\n            like float64 to float32, are allowed.\n          * 'unsafe' means any data conversions may be done.\n\n        Default is 'safe'.\n    optimize : {False, True, 'greedy', 'optimal'}, optional\n        Controls if intermediate optimization should occur. No optimization\n        will occur if False and True will default to the 'greedy' algorithm.\n        Also accepts an explicit contraction list from the ``np.einsum_path``\n        function. See ``np.einsum_path`` for more details. Default is True.\n\n    Returns\n    -------\n    output : ndarray\n        The calculation based on the Einstein summation convention.\n\n    See Also\n    --------\n    einsum_path, dot, inner, outer, tensordot, linalg.multi_dot\n\n    Notes\n    -----\n    .. versionadded:: 1.6.0\n\n    The subscripts string is a comma-separated list of subscript labels,\n    where each label refers to a dimension of the corresponding operand.\n    Repeated subscripts labels in one operand take the diagonal.  For example,\n    ``np.einsum('ii', a)`` is equivalent to ``np.trace(a)``.\n\n    Whenever a label is repeated, it is summed, so ``np.einsum('i,i', a, b)``\n    is equivalent to ``np.inner(a,b)``.  If a label appears only once,\n    it is not summed, so ``np.einsum('i', a)`` produces a view of ``a``\n    with no changes.\n\n    The order of labels in the output is by default alphabetical.  This\n    means that ``np.einsum('ij', a)`` doesn't affect a 2D array, while\n    ``np.einsum('ji', a)`` takes its transpose.\n\n    The output can be controlled by specifying output subscript labels\n    as well.  This specifies the label order, and allows summing to\n    be disallowed or forced when desired.  The call ``np.einsum('i->', a)``\n    is like ``np.sum(a, axis=-1)``, and ``np.einsum('ii->i', a)``\n    is like ``np.diag(a)``.  The difference is that `einsum` does not\n    allow broadcasting by default.\n\n    To enable and control broadcasting, use an ellipsis.  Default\n    NumPy-style broadcasting is done by adding an ellipsis\n    to the left of each term, like ``np.einsum('...ii->...i', a)``.\n    To take the trace along the first and last axes,\n    you can do ``np.einsum('i...i', a)``, or to do a matrix-matrix\n    product with the left-most indices instead of rightmost, you can do\n    ``np.einsum('ij...,jk...->ik...', a, b)``.\n\n    When there is only one operand, no axes are summed, and no output\n    parameter is provided, a view into the operand is returned instead\n    of a new array.  Thus, taking the diagonal as ``np.einsum('ii->i', a)``\n    produces a view.\n\n    An alternative way to provide the subscripts and operands is as\n    ``einsum(op0, sublist0, op1, sublist1, ..., [sublistout])``. The examples\n    below have corresponding `einsum` calls with the two parameter methods.\n\n    .. versionadded:: 1.10.0\n\n    Views returned from einsum are now writeable whenever the input array\n    is writeable. For example, ``np.einsum('ijk...->kji...', a)`` will now\n    have the same effect as ``np.swapaxes(a, 0, 2)`` and\n    ``np.einsum('ii->i', a)`` will return a writeable view of the diagonal\n    of a 2D array.\n\n    .. versionadded:: 1.12.0\n\n    Added the ``optimize`` argument which will optimize the contraction order\n    of an einsum expression. For a contraction with three or more operands this\n    can greatly increase the computational efficiency at the cost of a larger\n    memory footprint during computation.\n\n    See ``np.einsum_path`` for more details.\n\n    Examples\n    --------\n    >>> a = np.arange(25).reshape(5,5)\n    >>> b = np.arange(5)\n    >>> c = np.arange(6).reshape(2,3)\n\n    >>> np.einsum('ii', a)\n    60\n    >>> np.einsum(a, [0,0])\n    60\n    >>> np.trace(a)\n    60\n\n    >>> np.einsum('ii->i', a)\n    array([ 0,  6, 12, 18, 24])\n    >>> np.einsum(a, [0,0], [0])\n    array([ 0,  6, 12, 18, 24])\n    >>> np.diag(a)\n    array([ 0,  6, 12, 18, 24])\n\n    >>> np.einsum('ij,j', a, b)\n    array([ 30,  80, 130, 180, 230])\n    >>> np.einsum(a, [0,1], b, [1])\n    array([ 30,  80, 130, 180, 230])\n    >>> np.dot(a, b)\n    array([ 30,  80, 130, 180, 230])\n    >>> np.einsum('...j,j', a, b)\n    array([ 30,  80, 130, 180, 230])\n\n    >>> np.einsum('ji', c)\n    array([[0, 3],\n           [1, 4],\n           [2, 5]])\n    >>> np.einsum(c, [1,0])\n    array([[0, 3],\n           [1, 4],\n           [2, 5]])\n    >>> c.T\n    array([[0, 3],\n           [1, 4],\n           [2, 5]])\n\n    >>> np.einsum('..., ...', 3, c)\n    array([[ 0,  3,  6],\n           [ 9, 12, 15]])\n    >>> np.einsum(',ij', 3, C)\n    array([[ 0,  3,  6],\n           [ 9, 12, 15]])\n    >>> np.einsum(3, [Ellipsis], c, [Ellipsis])\n    array([[ 0,  3,  6],\n           [ 9, 12, 15]])\n    >>> np.multiply(3, c)\n    array([[ 0,  3,  6],\n           [ 9, 12, 15]])\n\n    >>> np.einsum('i,i', b, b)\n    30\n    >>> np.einsum(b, [0], b, [0])\n    30\n    >>> np.inner(b,b)\n    30\n\n    >>> np.einsum('i,j', np.arange(2)+1, b)\n    array([[0, 1, 2, 3, 4],\n           [0, 2, 4, 6, 8]])\n    >>> np.einsum(np.arange(2)+1, [0], b, [1])\n    array([[0, 1, 2, 3, 4],\n           [0, 2, 4, 6, 8]])\n    >>> np.outer(np.arange(2)+1, b)\n    array([[0, 1, 2, 3, 4],\n           [0, 2, 4, 6, 8]])\n\n    >>> np.einsum('i...->...', a)\n    array([50, 55, 60, 65, 70])\n    >>> np.einsum(a, [0,Ellipsis], [Ellipsis])\n    array([50, 55, 60, 65, 70])\n    >>> np.sum(a, axis=0)\n    array([50, 55, 60, 65, 70])\n\n    >>> a = np.arange(60.).reshape(3,4,5)\n    >>> b = np.arange(24.).reshape(4,3,2)\n    >>> np.einsum('ijk,jil->kl', a, b)\n    array([[ 4400.,  4730.],\n           [ 4532.,  4874.],\n           [ 4664.,  5018.],\n           [ 4796.,  5162.],\n           [ 4928.,  5306.]])\n    >>> np.einsum(a, [0,1,2], b, [1,0,3], [2,3])\n    array([[ 4400.,  4730.],\n           [ 4532.,  4874.],\n           [ 4664.,  5018.],\n           [ 4796.,  5162.],\n           [ 4928.,  5306.]])\n    >>> np.tensordot(a,b, axes=([1,0],[0,1]))\n    array([[ 4400.,  4730.],\n           [ 4532.,  4874.],\n           [ 4664.,  5018.],\n           [ 4796.,  5162.],\n           [ 4928.,  5306.]])\n\n    >>> a = np.arange(6).reshape((3,2))\n    >>> b = np.arange(12).reshape((4,3))\n    >>> np.einsum('ki,jk->ij', a, b)\n    array([[10, 28, 46, 64],\n           [13, 40, 67, 94]])\n    >>> np.einsum('ki,...k->i...', a, b)\n    array([[10, 28, 46, 64],\n           [13, 40, 67, 94]])\n    >>> np.einsum('k...,jk', a, b)\n    array([[10, 28, 46, 64],\n           [13, 40, 67, 94]])\n\n    >>> # since version 1.10.0\n    >>> a = np.zeros((3, 3))\n    >>> np.einsum('ii->i', a)[:] = 1\n    >>> a\n    array([[ 1.,  0.,  0.],\n           [ 0.,  1.,  0.],\n           [ 0.,  0.,  1.]])\n\n    "
    optimize_arg = kwargs.pop('optimize', (len(operands) > 3))
    if (optimize_arg is False):
        return c_einsum(*operands, **kwargs)
    valid_einsum_kwargs = ['out', 'dtype', 'order', 'casting']
    einsum_kwargs = {k: v for (k, v) in kwargs.items() if (k in valid_einsum_kwargs)}
    valid_contract_kwargs = (['optimize'] + valid_einsum_kwargs)
    unknown_kwargs = [k for (k, v) in kwargs.items() if (k not in valid_contract_kwargs)]
    if len(unknown_kwargs):
        raise TypeError(('Did not understand the following kwargs: %s' % unknown_kwargs))
    specified_out = False
    out_array = einsum_kwargs.pop('out', None)
    if (out_array is not None):
        specified_out = True
    (operands, contraction_list) = einsum_path(*operands, optimize=optimize_arg, einsum_call=True)
    handle_out = False
    for (num, contraction) in enumerate(contraction_list):
        (inds, idx_rm, einsum_str, remaining, blas) = contraction
        tmp_operands = []
        for x in inds:
            tmp_operands.append(operands.pop(x))
        handle_out = (specified_out and ((num + 1) == len(contraction_list)))
        if blas:
            (input_str, results_index) = einsum_str.split('->')
            (input_left, input_right) = input_str.split(',')
            tensor_result = (input_left + input_right)
            for s in idx_rm:
                tensor_result = tensor_result.replace(s, '')
            (left_pos, right_pos) = ([], [])
            for s in idx_rm:
                left_pos.append(input_left.find(s))
                right_pos.append(input_right.find(s))
            new_view = tensordot(*tmp_operands, axes=(tuple(left_pos), tuple(right_pos)))
            if ((tensor_result != results_index) or handle_out):
                if handle_out:
                    einsum_kwargs['out'] = out_array
                new_view = c_einsum(((tensor_result + '->') + results_index), new_view, **einsum_kwargs)
        else:
            if handle_out:
                einsum_kwargs['out'] = out_array
            new_view = c_einsum(einsum_str, *tmp_operands, **einsum_kwargs)
        operands.append(new_view)
        del tmp_operands, new_view
    if specified_out:
        return out_array
    else:
        return operands[0]
