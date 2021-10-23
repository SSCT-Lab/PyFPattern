def _add_splines(c, b1, d, b2):
    'Construct c*b1 + d*b2.'
    if ((b1 == S.Zero) or (c == S.Zero)):
        rv = piecewise_fold((d * b2))
    elif ((b2 == S.Zero) or (d == S.Zero)):
        rv = piecewise_fold((c * b1))
    else:
        new_args = []
        p1 = piecewise_fold((c * b1))
        p2 = piecewise_fold((d * b2))
        p2args = list(p2.args[:(- 1)])
        for arg in p1.args[:(- 1)]:
            expr = arg.expr
            cond = arg.cond
            lower = cond.args[0].rhs
            for (i, arg2) in enumerate(p2args):
                expr2 = arg2.expr
                cond2 = arg2.cond
                lower_2 = cond2.args[0].rhs
                upper_2 = cond2.args[1].rhs
                if (cond2 == cond):
                    expr += expr2
                    del p2args[i]
                    break
                elif ((lower_2 < lower) and (upper_2 <= lower)):
                    new_args.append(arg2)
                    del p2args[i]
                    break
            new_args.append((expr, cond))
        new_args.extend(p2args)
        new_args.append((0, True))
        rv = Piecewise(*new_args)
    return rv.expand()