def from_yaml(data, file_name='<string>', show_content=True, vault_secrets=None):
    '\n    Creates a python datastructure from the given data, which can be either\n    a JSON or YAML string.\n    '
    new_data = None
    if isinstance(data, AnsibleUnicode):
        in_data = text_type(data)
    else:
        in_data = data
    try:
        new_data = json.loads(in_data)
    except Exception:
        try:
            new_data = _safe_load(in_data, file_name=file_name, vault_secrets=vault_secrets)
        except YAMLError as yaml_exc:
            _handle_error(yaml_exc, file_name, show_content)
        if isinstance(data, AnsibleUnicode):
            new_data = AnsibleUnicode(new_data)
            new_data.ansible_pos = data.ansible_pos
    return new_data