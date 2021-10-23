

def caches_setting_for_tests(base=None, **params):
    base = (base or {
        
    })
    setting = {k: base.copy() for k in _caches_setting_base.keys()}
    for (key, cache_params) in setting.items():
        cache_params.update(_caches_setting_base[key])
        cache_params.update(params)
    return setting
