

def read_sql_table(table_name, con, schema=None, index_col=None, coerce_float=True, parse_dates=None, columns=None, chunksize=None):
    'Read SQL database table into a DataFrame.\n\n    Given a table name and a SQLAlchemy connectable, returns a DataFrame.\n    This function does not support DBAPI connections.\n\n    Parameters\n    ----------\n    table_name : string\n        Name of SQL table in database.\n    con : SQLAlchemy connectable (or database string URI)\n        SQLite DBAPI connection mode not supported.\n    schema : string, default None\n        Name of SQL schema in database to query (if database flavor\n        supports this). Uses default schema if None (default).\n    index_col : string or list of strings, optional, default: None\n        Column(s) to set as index(MultiIndex).\n    coerce_float : boolean, default True\n        Attempts to convert values of non-string, non-numeric objects (like\n        decimal.Decimal) to floating point. Can result in loss of Precision.\n    parse_dates : list or dict, default: None\n        - List of column names to parse as dates.\n        - Dict of ``{column_name: format string}`` where format string is\n          strftime compatible in case of parsing string times or is one of\n          (D, s, ns, ms, us) in case of parsing integer timestamps.\n        - Dict of ``{column_name: arg dict}``, where the arg dict corresponds\n          to the keyword arguments of :func:`pandas.to_datetime`\n          Especially useful with databases without native Datetime support,\n          such as SQLite.\n    columns : list, default: None\n        List of column names to select from SQL table\n    chunksize : int, default None\n        If specified, returns an iterator where `chunksize` is the number of\n        rows to include in each chunk.\n\n    Returns\n    -------\n    DataFrame\n\n    See Also\n    --------\n    read_sql_query : Read SQL query into a DataFrame.\n    read_sql\n\n    Notes\n    -----\n    Any datetime values with time zone information will be converted to UTC.\n    '
    con = _engine_builder(con)
    if (not _is_sqlalchemy_connectable(con)):
        raise NotImplementedError('read_sql_table only supported for SQLAlchemy connectable.')
    import sqlalchemy
    from sqlalchemy.schema import MetaData
    meta = MetaData(con, schema=schema)
    try:
        meta.reflect(only=[table_name], views=True)
    except sqlalchemy.exc.InvalidRequestError:
        raise ValueError('Table {name} not found'.format(name=table_name))
    pandas_sql = SQLDatabase(con, meta=meta)
    table = pandas_sql.read_table(table_name, index_col=index_col, coerce_float=coerce_float, parse_dates=parse_dates, columns=columns, chunksize=chunksize)
    if (table is not None):
        return table
    else:
        raise ValueError('Table {name} not found'.format(name=table_name), con)
