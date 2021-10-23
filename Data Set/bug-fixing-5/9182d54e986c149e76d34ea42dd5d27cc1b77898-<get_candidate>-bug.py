def get_candidate(module):
    candidate = NetworkConfig(indent=1)
    if module.params['src']:
        config = conversion_src(module)
        candidate.load(config)
    elif module.params['lines']:
        parents = (module.params['parents'] or list())
        candidate.add(module.params['lines'], parents=parents)
    return candidate