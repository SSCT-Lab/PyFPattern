def caches_setting_for_tests(base=None, exclude=None, **params):
    base = (base or {
        
    })
    exclude = (exclude or set())
    setting = {k: base.copy() for k in _caches_setting_base.keys() if (k not in exclude)}
    for (key, cache_params) in setting.items():
        cache_params.update(_caches_setting_base[key])
        cache_params.update(params)
    return setting