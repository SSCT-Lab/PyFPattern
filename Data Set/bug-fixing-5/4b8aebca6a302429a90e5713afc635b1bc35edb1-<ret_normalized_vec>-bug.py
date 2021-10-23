def ret_normalized_vec(vec, length):
    if (length != 1.0):
        return [(termid, (val / length)) for (termid, val) in vec]
    else:
        return list(vec)