def _check_warnings(warn_list, expected_type, expected_len):
    '\n    Checks that all of the warnings from a list returned by\n    `warnings.catch_all(record=True)` are of the required type and that the list\n    contains expected number of warnings.\n    '
    assert_equal(len(warn_list), expected_len, 'number of warnings')
    for warn_ in warn_list:
        assert_((warn_.category is expected_type))