def _groupby_and_merge(by, on, left, right, _merge_pieces, check_duplicates=True):
    '\n    groupby & merge; we are always performing a left-by type operation\n\n    Parameters\n    ----------\n    by: field to group\n    on: duplicates field\n    left: left frame\n    right: right frame\n    _merge_pieces: function for merging\n    check_duplicates: bool, default True\n        should we check & clean duplicates\n    '
    pieces = []
    if (not isinstance(by, (list, tuple))):
        by = [by]
    lby = left.groupby(by, sort=False)
    try:
        if check_duplicates:
            if (on is None):
                on = []
            elif (not isinstance(on, (list, tuple))):
                on = [on]
            if right.duplicated((by + on)).any():
                right = right.drop_duplicates((by + on), keep='last')
        rby = right.groupby(by, sort=False)
    except KeyError:
        rby = None
    for (key, lhs) in lby:
        if (rby is None):
            rhs = right
        else:
            try:
                rhs = right.take(rby.indices[key])
            except KeyError:
                lcols = lhs.columns.tolist()
                cols = (lcols + [r for r in right.columns if (r not in set(lcols))])
                merged = lhs.reindex(columns=cols)
                merged.index = range(len(merged))
                pieces.append(merged)
                continue
        merged = _merge_pieces(lhs, rhs)
        for k in by:
            try:
                if (k in merged):
                    merged[k] = key
            except KeyError:
                pass
        pieces.append(merged)
    from pandas.core.reshape.concat import concat
    result = concat(pieces, ignore_index=True)
    result = result.reindex(columns=pieces[0].columns, copy=False)
    return (result, lby)