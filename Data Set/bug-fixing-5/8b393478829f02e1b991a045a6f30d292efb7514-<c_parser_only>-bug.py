@pytest.fixture(params=_c_parsers_only, ids=_c_parser_ids)
def c_parser_only(request):
    return request.param