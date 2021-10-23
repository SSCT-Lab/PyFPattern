def _parameterize_test_case_generator(base, params):
    for (i, param) in enumerate(params):
        (yield _parameterize_test_case(base, i, param))