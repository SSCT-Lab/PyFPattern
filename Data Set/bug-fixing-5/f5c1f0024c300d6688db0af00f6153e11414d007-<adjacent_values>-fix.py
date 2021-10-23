def adjacent_values(vals, q1, q3):
    upper_adjacent_value = (q3 + ((q3 - q1) * 1.5))
    upper_adjacent_value = np.clip(upper_adjacent_value, q3, vals[(- 1)])
    lower_adjacent_value = (q1 - ((q3 - q1) * 1.5))
    lower_adjacent_value = np.clip(lower_adjacent_value, vals[0], q1)
    return (lower_adjacent_value, upper_adjacent_value)