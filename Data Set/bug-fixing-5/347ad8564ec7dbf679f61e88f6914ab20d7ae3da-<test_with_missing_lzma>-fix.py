def test_with_missing_lzma():
    'Tests if import pandas works when lzma is not present.'
    code = textwrap.dedent("        import sys\n        sys.modules['lzma'] = None\n        import pandas\n        ")
    subprocess.check_output([sys.executable, '-c', code])