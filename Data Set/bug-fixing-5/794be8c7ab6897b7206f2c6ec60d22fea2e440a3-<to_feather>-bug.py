def to_feather(df, path):
    '\n    Write a DataFrame to the feather-format\n\n    Parameters\n    ----------\n    df : DataFrame\n    path : string file path, or file-like object\n\n    '
    import_optional_dependency('pyarrow')
    from pyarrow import feather
    path = _stringify_path(path)
    if (not isinstance(df, DataFrame)):
        raise ValueError('feather only support IO with DataFrames')
    valid_types = {'string', 'unicode'}
    if (not isinstance(df.index, Int64Index)):
        raise ValueError('feather does not support serializing {} for the index; you can .reset_index()to make the index into column(s)'.format(type(df.index)))
    if (not df.index.equals(RangeIndex.from_range(range(len(df))))):
        raise ValueError('feather does not support serializing a non-default index for the index; you can .reset_index() to make the index into column(s)')
    if (df.index.name is not None):
        raise ValueError('feather does not serialize index meta-data on a default index')
    if (df.columns.inferred_type not in valid_types):
        raise ValueError('feather must have string column names')
    feather.write_feather(df, path)