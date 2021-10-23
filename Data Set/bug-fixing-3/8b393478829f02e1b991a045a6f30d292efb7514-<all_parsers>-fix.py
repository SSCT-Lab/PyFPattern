@pytest.fixture(params=_all_parsers, ids=_all_parser_ids)
def all_parsers(request):
    '\n    Fixture all of the CSV parsers.\n    '
    return request.param