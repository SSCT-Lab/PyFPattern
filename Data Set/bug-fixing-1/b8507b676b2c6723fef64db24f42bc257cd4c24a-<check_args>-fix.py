

def check_args(module, warnings):
    provider = (module.params['provider'] or {
        
    })
    for key in junos_argument_spec:
        if ((key not in ('provider',)) and module.params[key]):
            warnings.append(('argument %s has been deprecated and will be removed in a future version' % key))
    if provider:
        for param in ('password',):
            if provider.get(param):
                module.no_log_values.update(return_values(provider[param]))
