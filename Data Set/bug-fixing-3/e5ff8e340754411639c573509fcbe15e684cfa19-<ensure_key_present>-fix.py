def ensure_key_present(module, session, name, pubkey, force, check_mode):
    all_keys = get_all_keys(session)
    matching_keys = [k for k in all_keys if (k['title'] == name)]
    deleted_keys = []
    new_signature = pubkey.split(' ')[1]
    for key in all_keys:
        existing_signature = key['key'].split(' ')[1]
        if ((new_signature == existing_signature) and (key['title'] != name)):
            module.fail_json(msg='another key with the same content is already registered under the name |{}|'.format(key['title']))
    if (matching_keys and force and (matching_keys[0]['key'].split(' ')[1] != new_signature)):
        delete_keys(session, matching_keys, check_mode=check_mode)
        (deleted_keys, matching_keys) = (matching_keys, [])
    if (not matching_keys):
        key = create_key(session, name, pubkey, check_mode=check_mode)
    else:
        key = matching_keys[0]
    return {
        'changed': bool((deleted_keys or (not matching_keys))),
        'deleted_keys': deleted_keys,
        'matching_keys': matching_keys,
        'key': key,
    }