def render_fixture(self, function: str, name: Optional[str]=None) -> List[str]:
    fixture = []
    if name:
        fixture_dict = zerver.lib.api_test_helpers.FIXTURES[function][name]
    else:
        fixture_dict = zerver.lib.api_test_helpers.FIXTURES[function]
    fixture_json = json.dumps(fixture_dict, indent=4, sort_keys=True, separators=(',', ': '))
    fixture.append('```')
    fixture.extend(fixture_json.splitlines())
    fixture.append('```')
    return fixture