def load_extra_vars(loader, options):
    extra_vars = {
        
    }
    for extra_vars_opt in options.extra_vars:
        extra_vars_opt = to_text(extra_vars_opt, errors='surrogate_or_strict')
        if extra_vars_opt.startswith('@'):
            data = loader.load_from_file(extra_vars_opt[1:])
        elif (extra_vars_opt and (extra_vars_opt[0] in '[{')):
            data = loader.load(extra_vars_opt)
        else:
            data = parse_kv(extra_vars_opt)
        extra_vars = combine_vars(extra_vars, data)
    return extra_vars