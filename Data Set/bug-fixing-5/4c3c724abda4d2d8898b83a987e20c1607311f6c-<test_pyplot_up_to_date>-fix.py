def test_pyplot_up_to_date():
    gen_script = (Path(mpl.__file__).parents[2] / 'tools/boilerplate.py')
    if (not gen_script.exists()):
        pytest.skip('boilerplate.py not found')
    orig_contents = Path(plt.__file__).read_text()
    try:
        subprocess.run([sys.executable, str(gen_script)], check=True)
        new_contents = Path(plt.__file__).read_text()
        if (orig_contents != new_contents):
            diff_msg = '\n'.join(difflib.unified_diff(orig_contents.split('\n'), new_contents.split('\n'), fromfile='found pyplot.py', tofile='expected pyplot.py', n=0, lineterm=''))
            pytest.fail(("pyplot.py is not up-to-date. Please run 'python tools/boilerplate.py' to update pyplot.py. This needs to be done from an environment where your current working copy is installed (e.g. 'pip install -e'd). Here is a diff of unexpected differences:\n%s" % diff_msg))
    finally:
        Path(plt.__file__).write_text(orig_contents)