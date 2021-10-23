def get_user_diff(client, ipa_user, module_user):
    '\n        Return the keys of each dict whereas values are different. Unfortunately the IPA\n        API returns everything as a list even if only a single value is possible.\n        Therefore some more complexity is needed.\n        The method will check if the value type of module_user.attr is not a list and\n        create a list with that element if the same attribute in ipa_user is list. In this way I hope that the method\n        must not be changed if the returned API dict is changed.\n    :param ipa_user:\n    :param module_user:\n    :return:\n    '
    sshpubkey = None
    if ('ipasshpubkey' in module_user):
        hash_algo = 'md5'
        if (('sshpubkeyfp' in ipa_user) and (ipa_user['sshpubkeyfp'][0][:7].upper() == 'SHA256:')):
            hash_algo = 'sha256'
        module_user['sshpubkeyfp'] = [get_ssh_key_fingerprint(pubkey, hash_algo) for pubkey in module_user['ipasshpubkey']]
        sshpubkey = module_user['ipasshpubkey']
        del module_user['ipasshpubkey']
    result = client.get_diff(ipa_data=ipa_user, module_data=module_user)
    if (sshpubkey is not None):
        del module_user['sshpubkeyfp']
        module_user['ipasshpubkey'] = sshpubkey
    return result