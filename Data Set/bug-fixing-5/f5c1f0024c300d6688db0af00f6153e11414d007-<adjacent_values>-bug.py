def adjacent_values(vals):
    q1 = percentile(vals, 0.25)
    q3 = percentile(vals, 0.75)
    iqr = (q3 - q1)
    uav = (q3 + (iqr * 1.5))
    if (uav > vals[(- 1)]):
        uav = vals[(- 1)]
    if (uav < q3):
        uav = q3
    lav = (q1 - (iqr * 1.5))
    if (lav < vals[0]):
        lav = vals[0]
    if (lav > q1):
        lav = q1
    return [lav, uav]