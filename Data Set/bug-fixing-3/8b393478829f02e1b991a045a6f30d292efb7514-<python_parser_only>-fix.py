@pytest.fixture(params=_py_parsers_only, ids=_py_parser_ids)
def python_parser_only(request):
    '\n    Fixture all of the CSV parsers using the Python engine.\n    '
    return request.param