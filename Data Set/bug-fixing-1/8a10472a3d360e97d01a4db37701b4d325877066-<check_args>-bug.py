

def check_args(module):
    provider = (module.params['provider'] or {
        
    })
    for key in asa_argument_spec:
        if ((key not in ['provider', 'authorize']) and module.params[key]):
            module.warn(('argument %s has been deprecated and will be removed in a future version' % key))
    if provider:
        for param in ('auth_pass', 'password'):
            if provider.get(param):
                module.no_log_values.update(return_values(provider[param]))
