def test_with_missing_lzma_runtime():
    'Tests if RuntimeError is hit when calling lzma without\n    having the module available.'
    code = textwrap.dedent("\n        import sys\n        import pytest\n        sys.modules['lzma'] = None\n        import pandas\n        df = pandas.DataFrame()\n        with pytest.raises(RuntimeError, match='lzma module'):\n            df.to_csv('foo.csv', compression='xz')\n        ")
    subprocess.check_output([sys.executable, '-c', code])