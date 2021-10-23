@pytest.fixture(params=_c_parsers_only, ids=_c_parser_ids)
def c_parser_only(request):
    '\n    Fixture all of the CSV parsers using the C engine.\n    '
    return request.param