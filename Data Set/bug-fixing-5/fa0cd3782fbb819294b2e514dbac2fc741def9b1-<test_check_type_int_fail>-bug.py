def test_check_type_int_fail():
    test_cases = ({
        'k1': 'v1',
    }, (b'1', 1), (3.14159, 3), 'b')
    for case in test_cases:
        with pytest.raises(TypeError) as e:
            check_type_int(case)
    assert ('cannot be converted to an int' in to_native(e))