

def get_candidate(module):
    candidate = NetworkConfig(indent=1)
    if module.params['src']:
        try:
            candidate.loadfp(module.params['src'])
        except IOError:
            candidate.load(module.params['src'])
    elif module.params['lines']:
        parents = (module.params['parents'] or list())
        candidate.add(module.params['lines'], parents=parents)
    return candidate
