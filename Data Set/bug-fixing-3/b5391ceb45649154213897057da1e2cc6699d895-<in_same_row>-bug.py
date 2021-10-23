def in_same_row(ss0, ssc):
    (nrows, ncols) = ss0.get_gridspec().get_geometry()
    if (ss0.num2 is None):
        ss0.num2 = ss0.num1
    (rownum0min, colnum0min) = divmod(ss0.num1, ncols)
    (rownum0max, colnum0max) = divmod(ss0.num2, ncols)
    if (ssc.num2 is None):
        ssc.num2 = ssc.num1
    (rownumCmin, colnumCmin) = divmod(ssc.num1, ncols)
    (rownumCmax, colnumCmax) = divmod(ssc.num2, ncols)
    if ((rownum0min >= rownumCmin) and (rownum0min <= rownumCmax)):
        return True
    if ((rownum0max >= rownumCmin) and (rownum0max <= rownumCmax)):
        return True
    return False