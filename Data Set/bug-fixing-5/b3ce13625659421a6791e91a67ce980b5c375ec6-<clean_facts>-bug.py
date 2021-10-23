def clean_facts(facts):
    ' remove facts that can override internal keys or othewise deemed unsafe '
    data = deepcopy(facts)
    remove_keys = set()
    fact_keys = set(data.keys())
    for magic_var in C.MAGIC_VARIABLE_MAPPING:
        remove_keys.update(fact_keys.intersection(C.MAGIC_VARIABLE_MAPPING[magic_var]))
    for conn_path in connection_loader.all(path_only=True):
        try:
            conn_name = os.path.splitext(os.path.basename(conn_path))[0]
            re_key = re.compile(('^ansible_%s_' % conn_name))
            for fact_key in fact_keys:
                if (re_key.match(fact_key) and (not fact_key.endswith(('_bridge', '_gwbridge')))):
                    remove_keys.add(fact_key)
        except AttributeError:
            pass
    for hard in (C.RESTRICTED_RESULT_KEYS + C.INTERNAL_RESULT_KEYS):
        if (hard in fact_keys):
            remove_keys.add(hard)
    re_interp = re.compile('^ansible_.*_interpreter$')
    for fact_key in fact_keys:
        if re_interp.match(fact_key):
            remove_keys.add(fact_key)
    for r_key in remove_keys:
        if (not r_key.startswith('ansible_ssh_host_key_')):
            try:
                r_val = to_text(data[r_key])
                if (len(r_val) > 24):
                    r_val = ('%s ... %s' % (r_val[:13], r_val[(- 6):]))
            except Exception:
                r_val = ' <failed to convert value to a string> '
            display.warning(('Removed restricted key from module data: %s = %s' % (r_key, r_val)))
            del data[r_key]
    return strip_internal_keys(data)