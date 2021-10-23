def _line_profile_coordinates(src, dst, linewidth=1):
    'Return the coordinates of the profile of an image along a scan line.\n\n    Parameters\n    ----------\n    src : 2-tuple of numeric scalar (float or int)\n        The start point of the scan line.\n    dst : 2-tuple of numeric scalar (float or int)\n        The end point of the scan line.\n    linewidth : int, optional\n        Width of the scan, perpendicular to the line\n\n    Returns\n    -------\n    coords : array, shape (2, N, C), float\n        The coordinates of the profile along the scan line. The length of the\n        profile is the ceil of the computed length of the scan line.\n\n    Notes\n    -----\n    This is a utility method meant to be used internally by skimage functions.\n    The destination point is included in the profile, in contrast to\n    standard numpy indexing.\n    '
    (src_row, src_col) = src = np.asarray(src, dtype=float)
    (dst_row, dst_col) = dst = np.asarray(dst, dtype=float)
    (d_row, d_col) = (dst - src)
    theta = np.arctan2(d_row, d_col)
    length = np.ceil((np.hypot(d_row, d_col) + 1))
    line_col = np.linspace(src_col, dst_col, length)
    line_row = np.linspace(src_row, dst_row, length)
    col_width = (((linewidth - 1) * np.sin((- theta))) / 2)
    row_width = (((linewidth - 1) * np.cos(theta)) / 2)
    perp_rows = np.array([np.linspace((row_i - row_width), (row_i + row_width), linewidth) for row_i in line_row])
    perp_cols = np.array([np.linspace((col_i - col_width), (col_i + col_width), linewidth) for col_i in line_col])
    return np.array([perp_rows, perp_cols])