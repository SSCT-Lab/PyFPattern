def _add_splines(c, b1, d, b2):
    'Construct c*b1 + d*b2.'
    if ((b1 == S.Zero) or (c == S.Zero)):
        rv = piecewise_fold((d * b2))
    elif ((b2 == S.Zero) or (d == S.Zero)):
        rv = piecewise_fold((c * b1))
    else:
        new_args = []
        n_intervals = len(b1.args)
        if (n_intervals != len(b2.args)):
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
        else:
            new_args.append(((c * b1.args[0].expr), b1.args[0].cond))
            for i in range(1, (n_intervals - 1)):
                new_args.append((((c * b1.args[i].expr) + (d * b2.args[(i - 1)].expr)), b1.args[i].cond))
            new_args.append(((d * b2.args[(- 2)].expr), b2.args[(- 2)].cond))
            new_args.append(b2.args[(- 1)])
        rv = Piecewise(*new_args)
    return rv.expand()