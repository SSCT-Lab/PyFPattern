def test_missing_required_dependency(monkeypatch):
    original_import = __import__

    def mock_import_fail(name, *args, **kwargs):
        if (name == 'numpy'):
            raise ImportError('cannot import name numpy')
        elif (name == 'pytz'):
            raise ImportError('cannot import name some_dependency')
        elif (name == 'dateutil'):
            raise ImportError('cannot import name some_other_dependency')
        else:
            return original_import(name, *args, **kwargs)
    expected_msg = 'Unable to import required dependencies:\nnumpy: cannot import name numpy\npytz: cannot import name some_dependency\ndateutil: cannot import name some_other_dependency'
    import pandas as pd
    with monkeypatch.context() as m:
        m.setattr(builtins, '__import__', mock_import_fail)
        with pytest.raises(ImportError, match=expected_msg):
            importlib.reload(pd)