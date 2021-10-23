def namespace_facts(facts):
    " return all facts inside 'ansible_facts' w/o an ansible_ prefix "
    deprefixed = {
        
    }
    for k in facts:
        if (k in 'ansible_local'):
            deprefixed[k] = deepcopy(facts[k])
        else:
            deprefixed[k.replace('ansible_', '', 1)] = deepcopy(facts[k])
    return {
        'ansible_facts': deprefixed,
    }