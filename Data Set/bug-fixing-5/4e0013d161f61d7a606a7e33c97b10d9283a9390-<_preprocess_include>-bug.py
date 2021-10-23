def _preprocess_include(self, ds, new_ds, k, v):
    '\n        Splits the include line up into filename and parameters\n        '
    items = split_args(v)
    if (len(items) == 0):
        raise AnsibleParserError('include statements must specify the file name to include', obj=ds)
    else:
        new_ds['include'] = items[0]
        if (len(items) > 1):
            params = parse_kv(' '.join(items[1:]))
            if ('tags' in params):
                new_ds['tags'] = params.pop('tags')
            if ('vars' in new_ds):
                raise AnsibleParserError("include parameters cannot be mixed with 'vars' entries for include statements", obj=ds)
            new_ds['vars'] = params