def load_extra_vars(loader, options):
    extra_vars = {
        
    }
    for extra_vars_opt in options.extra_vars:
        data = None
        extra_vars_opt = to_text(extra_vars_opt, errors='surrogate_or_strict')
        if extra_vars_opt.startswith('@'):
            data = loader.load_from_file(extra_vars_opt[1:])
        elif (extra_vars_opt and (extra_vars_opt[0] in '[{')):
            data = loader.load(extra_vars_opt)
        else:
            data = parse_kv(extra_vars_opt)
        if isinstance(data, MutableMapping):
            extra_vars = combine_vars(extra_vars, data)
        else:
            raise AnsibleOptionsError(("Invalid extra vars data supplied. '%s' could not be made into a dictionary" % extra_vars_opt))
    return extra_vars