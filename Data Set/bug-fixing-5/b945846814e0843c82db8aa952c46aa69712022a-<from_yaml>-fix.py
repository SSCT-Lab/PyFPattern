def from_yaml(data, file_name='<string>', show_content=True, vault_secrets=None):
    '\n    Creates a python datastructure from the given data, which can be either\n    a JSON or YAML string.\n    '
    new_data = None
    try:
        new_data = json.loads(data)
    except Exception:
        try:
            new_data = _safe_load(data, file_name=file_name, vault_secrets=vault_secrets)
        except YAMLError as yaml_exc:
            _handle_error(yaml_exc, file_name, show_content)
    return new_data