

def make_checks(loop_orders, dtypes, sub):
    init = ''
    for (i, (loop_order, dtype)) in enumerate(zip(loop_orders, dtypes)):
        var = ('%%(lv%i)s' % i)
        nonx = [x for x in loop_order if (x != 'x')]
        if nonx:
            min_nd = (max(nonx) + 1)
            init += ('\n            if (PyArray_NDIM(%(var)s) < %(min_nd)s) {\n                PyErr_SetString(PyExc_ValueError, "Not enough dimensions on input.");\n                %%(fail)s\n            }\n            ' % locals())
        adjust = '0'
        for (j, index) in reversed(list(enumerate(loop_order))):
            if (index != 'x'):
                jump = ('(%s) - (%s)' % (('%(var)s_stride%(index)s' % locals()), adjust))
                init += ('\n                %(var)s_n%(index)s = PyArray_DIMS(%(var)s)[%(index)s];\n                %(var)s_stride%(index)s = PyArray_STRIDES(%(var)s)[%(index)s] / sizeof(%(dtype)s);\n                %(var)s_jump%(index)s_%(j)s = %(jump)s;\n                //printf("%(var)s_jump%(index)s_%(j)s is:");\n                //std::cout << %(var)s_jump%(index)s_%(j)s << std::endl;\n                ' % locals())
                adjust = ('%(var)s_n%(index)s*%(var)s_stride%(index)s' % locals())
            else:
                jump = ('-(%s)' % adjust)
                init += ('\n                %(var)s_jump%(index)s_%(j)s = %(jump)s;\n                //printf("%(var)s_jump%(index)s_%(j)s is:");\n                //std::cout << %(var)s_jump%(index)s_%(j)s << std::endl;\n                ' % locals())
                adjust = '0'
    check = ''
    for matches in zip(*loop_orders):
        to_compare = [(j, x) for (j, x) in enumerate(matches) if (x != 'x')]
        if (len(to_compare) < 2):
            continue
        (j0, x0) = to_compare[0]
        for (j, x) in to_compare[1:]:
            check += ('\n            if (%%(lv%(j0)s)s_n%(x0)s != %%(lv%(j)s)s_n%(x)s)\n            {\n                PyErr_Format(PyExc_ValueError, "Input dimension mis-match. (input[%%%%i].shape[%%%%i] = %%%%lli, input[%%%%i].shape[%%%%i] = %%%%lli)",\n                   %(j0)s,\n                   %(x0)s,\n                   (long long int) %%(lv%(j0)s)s_n%(x0)s,\n                   %(j)s,\n                   %(x)s,\n                   (long long int) %%(lv%(j)s)s_n%(x)s\n                );\n                %%(fail)s\n            }\n            ' % locals())
    return ((init % sub) + (check % sub))
