

def _fill_mi_header(row, control_row):
    'Forward fills blank entries in row, but only inside the same parent index\n\n    Used for creating headers in Multiindex.\n    Parameters\n    ----------\n    row : list\n        List of items in a single row.\n    constrol_row : list of boolean\n        Helps to determine if particular column is in same parent index as the\n        previous value. Used to stop propagation of empty cells between\n        different indexes.\n\n    Returns\n    ----------\n    Returns changed row and control_row\n    '
    last = row[0]
    for i in range(1, len(row)):
        if (not control_row[i]):
            last = row[i]
        if ((row[i] == '') or (row[i] is None)):
            row[i] = last
        else:
            control_row[i] = False
            last = row[i]
    return (row, control_row)
