def ensure_key_present(session, name, pubkey, force, check_mode):
    matching_keys = [k for k in get_all_keys(session) if (k['title'] == name)]
    deleted_keys = []
    if (matching_keys and force and (matching_keys[0]['key'] != pubkey)):
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