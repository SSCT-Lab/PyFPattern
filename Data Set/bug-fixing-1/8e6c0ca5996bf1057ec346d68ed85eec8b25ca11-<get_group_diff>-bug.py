

def get_group_diff(client, ipa_group, module_group):
    data = []
    if ('nonposix' in module_group):
        if ((not module_group['nonposix']) and ipa_group.get('nonposix')):
            module_group['posix'] = True
        del module_group['nonposix']
    return client.get_diff(ipa_data=ipa_group, module_data=module_group)
