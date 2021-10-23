def test_missing_required_dependency():
    call = ['python', '-S', '-c', 'import pandas']
    with pytest.raises(subprocess.CalledProcessError) as exc:
        subprocess.check_output(call, stderr=subprocess.STDOUT)
    output = exc.value.stdout.decode()
    assert all(((x in output) for x in ['numpy', 'pytz', 'dateutil']))