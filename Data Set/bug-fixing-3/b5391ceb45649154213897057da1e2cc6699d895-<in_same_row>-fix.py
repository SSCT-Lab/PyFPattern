def in_same_row(rownum0min, rownum0max, rownumCmin, rownumCmax):
    if ((rownum0min >= rownumCmin) and (rownum0min <= rownumCmax)):
        return True
    if ((rownum0max >= rownumCmin) and (rownum0max <= rownumCmax)):
        return True
    return False