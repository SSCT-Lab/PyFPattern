def einsum_path(*operands, **kwargs):
    "\n    einsum_path(subscripts, *operands, optimize='greedy')\n\n    Evaluates the lowest cost contraction order for an einsum expression by\n    considering the creation of intermediate arrays.\n\n    Parameters\n    ----------\n    subscripts : str\n        Specifies the subscripts for summation.\n    *operands : list of array_like\n        These are the arrays for the operation.\n    optimize : {bool, list, tuple, 'greedy', 'optimal'}\n        Choose the type of path. If a tuple is provided, the second argument is\n        assumed to be the maximum intermediate size created. If only a single\n        argument is provided the largest input or output array size is used\n        as a maximum intermediate size.\n\n        * if a list is given that starts with ``einsum_path``, uses this as the\n          contraction path\n        * if False no optimization is taken\n        * if True defaults to the 'greedy' algorithm\n        * 'optimal' An algorithm that combinatorially explores all possible\n          ways of contracting the listed tensors and choosest the least costly\n          path. Scales exponentially with the number of terms in the\n          contraction.\n        * 'greedy' An algorithm that chooses the best pair contraction\n          at each step. Effectively, this algorithm searches the largest inner,\n          Hadamard, and then outer products at each step. Scales cubically with\n          the number of terms in the contraction. Equivalent to the 'optimal'\n          path for most contractions.\n\n        Default is 'greedy'.\n\n    Returns\n    -------\n    path : list of tuples\n        A list representation of the einsum path.\n    string_repr : str\n        A printable representation of the einsum path.\n\n    Notes\n    -----\n    The resulting path indicates which terms of the input contraction should be\n    contracted first, the result of this contraction is then appended to the\n    end of the contraction list. This list can then be iterated over until all\n    intermediate contractions are complete.\n\n    See Also\n    --------\n    einsum, linalg.multi_dot\n\n    Examples\n    --------\n\n    We can begin with a chain dot example. In this case, it is optimal to\n    contract the ``b`` and ``c`` tensors first as reprsented by the first\n    element of the path ``(1, 2)``. The resulting tensor is added to the end\n    of the contraction and the remaining contraction ``(0, 1)`` is then\n    completed.\n\n    >>> a = np.random.rand(2, 2)\n    >>> b = np.random.rand(2, 5)\n    >>> c = np.random.rand(5, 2)\n    >>> path_info = np.einsum_path('ij,jk,kl->il', a, b, c, optimize='greedy')\n    >>> print(path_info[0])\n    ['einsum_path', (1, 2), (0, 1)]\n    >>> print(path_info[1])\n      Complete contraction:  ij,jk,kl->il\n             Naive scaling:  4\n         Optimized scaling:  3\n          Naive FLOP count:  1.600e+02\n      Optimized FLOP count:  5.600e+01\n       Theoretical speedup:  2.857\n      Largest intermediate:  4.000e+00 elements\n    -------------------------------------------------------------------------\n    scaling                  current                                remaining\n    -------------------------------------------------------------------------\n       3                   kl,jk->jl                                ij,jl->il\n       3                   jl,ij->il                                   il->il\n\n\n    A more complex index transformation example.\n\n    >>> I = np.random.rand(10, 10, 10, 10)\n    >>> C = np.random.rand(10, 10)\n    >>> path_info = np.einsum_path('ea,fb,abcd,gc,hd->efgh', C, C, I, C, C,\n                                   optimize='greedy')\n\n    >>> print(path_info[0])\n    ['einsum_path', (0, 2), (0, 3), (0, 2), (0, 1)]\n    >>> print(path_info[1])\n      Complete contraction:  ea,fb,abcd,gc,hd->efgh\n             Naive scaling:  8\n         Optimized scaling:  5\n          Naive FLOP count:  8.000e+08\n      Optimized FLOP count:  8.000e+05\n       Theoretical speedup:  1000.000\n      Largest intermediate:  1.000e+04 elements\n    --------------------------------------------------------------------------\n    scaling                  current                                remaining\n    --------------------------------------------------------------------------\n       5               abcd,ea->bcde                      fb,gc,hd,bcde->efgh\n       5               bcde,fb->cdef                         gc,hd,cdef->efgh\n       5               cdef,gc->defg                            hd,defg->efgh\n       5               defg,hd->efgh                               efgh->efgh\n    "
    valid_contract_kwargs = ['optimize', 'einsum_call']
    unknown_kwargs = [k for (k, v) in kwargs.items() if (k not in valid_contract_kwargs)]
    if len(unknown_kwargs):
        raise TypeError(('Did not understand the following kwargs: %s' % unknown_kwargs))
    path_type = kwargs.pop('optimize', True)
    if (path_type is True):
        path_type = 'greedy'
    if (path_type is None):
        path_type = False
    memory_limit = None
    if ((path_type is False) or isinstance(path_type, basestring)):
        pass
    elif (len(path_type) and (path_type[0] == 'einsum_path')):
        pass
    elif ((len(path_type) == 2) and isinstance(path_type[0], basestring) and isinstance(path_type[1], (int, float))):
        memory_limit = int(path_type[1])
        path_type = path_type[0]
    else:
        raise TypeError(('Did not understand the path: %s' % str(path_type)))
    einsum_call_arg = kwargs.pop('einsum_call', False)
    (input_subscripts, output_subscript, operands) = _parse_einsum_input(operands)
    subscripts = ((input_subscripts + '->') + output_subscript)
    input_list = input_subscripts.split(',')
    input_sets = [set(x) for x in input_list]
    output_set = set(output_subscript)
    indices = set(input_subscripts.replace(',', ''))
    dimension_dict = {
        
    }
    for (tnum, term) in enumerate(input_list):
        sh = operands[tnum].shape
        if (len(sh) != len(term)):
            raise ValueError('Einstein sum subscript %s does not contain the correct number of indices for operand %d.', input_subscripts[tnum], tnum)
        for (cnum, char) in enumerate(term):
            dim = sh[cnum]
            if (char in dimension_dict.keys()):
                if (dimension_dict[char] != dim):
                    raise ValueError("Size of label '%s' for operand %d does not match previous terms.", char, tnum)
            else:
                dimension_dict[char] = dim
    size_list = []
    for term in (input_list + [output_subscript]):
        size_list.append(_compute_size_by_dict(term, dimension_dict))
    max_size = max(size_list)
    if (memory_limit is None):
        memory_arg = max_size
    else:
        memory_arg = memory_limit
    naive_cost = _compute_size_by_dict(indices, dimension_dict)
    indices_in_input = input_subscripts.replace(',', '')
    mult = max((len(input_list) - 1), 1)
    if (len(indices_in_input) - len(set(indices_in_input))):
        mult *= 2
    naive_cost *= mult
    if ((path_type is False) or (len(input_list) in [1, 2]) or (indices == output_set)):
        path = [tuple(range(len(input_list)))]
    elif (path_type == 'greedy'):
        memory_arg = min(memory_arg, max_size)
        path = _greedy_path(input_sets, output_set, dimension_dict, memory_arg)
    elif (path_type == 'optimal'):
        path = _optimal_path(input_sets, output_set, dimension_dict, memory_arg)
    elif (path_type[0] == 'einsum_path'):
        path = path_type[1:]
    else:
        raise KeyError('Path name %s not found', path_type)
    (cost_list, scale_list, size_list, contraction_list) = ([], [], [], [])
    for (cnum, contract_inds) in enumerate(path):
        contract_inds = tuple(sorted(list(contract_inds), reverse=True))
        contract = _find_contraction(contract_inds, input_sets, output_set)
        (out_inds, input_sets, idx_removed, idx_contract) = contract
        cost = _compute_size_by_dict(idx_contract, dimension_dict)
        if idx_removed:
            cost *= 2
        cost_list.append(cost)
        scale_list.append(len(idx_contract))
        size_list.append(_compute_size_by_dict(out_inds, dimension_dict))
        tmp_inputs = []
        for x in contract_inds:
            tmp_inputs.append(input_list.pop(x))
        do_blas = _can_dot(tmp_inputs, out_inds, idx_removed)
        if ((cnum - len(path)) == (- 1)):
            idx_result = output_subscript
        else:
            sort_result = [(dimension_dict[ind], ind) for ind in out_inds]
            idx_result = ''.join([x[1] for x in sorted(sort_result)])
        input_list.append(idx_result)
        einsum_str = ((','.join(tmp_inputs) + '->') + idx_result)
        contraction = (contract_inds, idx_removed, einsum_str, input_list[:], do_blas)
        contraction_list.append(contraction)
    opt_cost = (sum(cost_list) + 1)
    if einsum_call_arg:
        return (operands, contraction_list)
    overall_contraction = ((input_subscripts + '->') + output_subscript)
    header = ('scaling', 'current', 'remaining')
    speedup = (naive_cost / opt_cost)
    max_i = max(size_list)
    path_print = ('  Complete contraction:  %s\n' % overall_contraction)
    path_print += ('         Naive scaling:  %d\n' % len(indices))
    path_print += ('     Optimized scaling:  %d\n' % max(scale_list))
    path_print += ('      Naive FLOP count:  %.3e\n' % naive_cost)
    path_print += ('  Optimized FLOP count:  %.3e\n' % opt_cost)
    path_print += ('   Theoretical speedup:  %3.3f\n' % speedup)
    path_print += ('  Largest intermediate:  %.3e elements\n' % max_i)
    path_print += (('-' * 74) + '\n')
    path_print += ('%6s %24s %40s\n' % header)
    path_print += ('-' * 74)
    for (n, contraction) in enumerate(contraction_list):
        (inds, idx_rm, einsum_str, remaining, blas) = contraction
        remaining_str = ((','.join(remaining) + '->') + output_subscript)
        path_run = (scale_list[n], einsum_str, remaining_str)
        path_print += ('\n%4d    %24s %40s' % path_run)
    path = (['einsum_path'] + path)
    return (path, path_print)