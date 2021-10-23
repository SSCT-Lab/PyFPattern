def get_engine(engine):
    ' return our implementation '
    if (engine == 'auto'):
        engine = get_option('io.parquet.engine')
    if (engine == 'auto'):
        try:
            return PyArrowImpl()
        except ImportError:
            pass
        try:
            return FastParquetImpl()
        except ImportError:
            pass
        raise ImportError("Unable to find a usable engine; tried using: 'pyarrow', 'fastparquet'.\npyarrow or fastparquet is required for parquet support")
    if (engine not in ['pyarrow', 'fastparquet']):
        raise ValueError("engine must be one of 'pyarrow', 'fastparquet'")
    if (engine == 'pyarrow'):
        return PyArrowImpl()
    elif (engine == 'fastparquet'):
        return FastParquetImpl()