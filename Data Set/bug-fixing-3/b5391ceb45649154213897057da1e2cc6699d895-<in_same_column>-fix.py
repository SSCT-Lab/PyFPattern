def in_same_column(colnum0min, colnum0max, colnumCmin, colnumCmax):
    if ((colnum0min >= colnumCmin) and (colnum0min <= colnumCmax)):
        return True
    if ((colnum0max >= colnumCmin) and (colnum0max <= colnumCmax)):
        return True
    return False