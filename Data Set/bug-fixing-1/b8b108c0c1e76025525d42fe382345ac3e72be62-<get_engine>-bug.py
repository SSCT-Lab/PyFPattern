

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
    if (engine not in ['pyarrow', 'fastparquet']):
        raise ValueError("engine must be one of 'pyarrow', 'fastparquet'")
    if (engine == 'pyarrow'):
        return PyArrowImpl()
    elif (engine == 'fastparquet'):
        return FastParquetImpl()
