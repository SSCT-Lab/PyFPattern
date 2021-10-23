def _preprocess_import(self, ds, new_ds, k, v):
    '\n        Splits the playbook import line up into filename and parameters\n        '
    if (v is None):
        raise AnsibleParserError('playbook import parameter is missing', obj=ds)
    items = split_args(v)
    if (len(items) == 0):
        raise AnsibleParserError('import_playbook statements must specify the file name to import', obj=ds)
    else:
        new_ds['import_playbook'] = items[0]
        if (len(items) > 1):
            params = parse_kv(' '.join(items[1:]))
            if ('tags' in params):
                new_ds['tags'] = params.pop('tags')
            if ('vars' in new_ds):
                raise AnsibleParserError("import_playbook parameters cannot be mixed with 'vars' entries for import statements", obj=ds)
            new_ds['vars'] = params