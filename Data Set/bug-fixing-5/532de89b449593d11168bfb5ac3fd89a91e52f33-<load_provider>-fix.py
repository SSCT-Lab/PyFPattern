def load_provider(spec, args):
    provider = args.get('provider', {
        
    })
    for (key, value) in iteritems(spec):
        if (key not in provider):
            if (key in args):
                provider[key] = args[key]
            elif ('fallback' in value):
                provider[key] = _fallback(value['fallback'])
            elif ('default' in value):
                provider[key] = value['default']
            else:
                provider[key] = None
    if ('authorize' in provider):
        provider['authorize'] = boolean((provider['authorize'] or False))
    args['provider'] = provider
    return provider