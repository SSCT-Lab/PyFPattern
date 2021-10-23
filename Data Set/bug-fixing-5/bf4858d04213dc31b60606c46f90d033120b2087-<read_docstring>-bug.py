def read_docstring(filename, verbose=True, ignore_errors=True):
    '\n    Search for assignment of the DOCUMENTATION and EXAMPLES variables in the given file.\n    Parse DOCUMENTATION from YAML and return the YAML doc or None together with EXAMPLES, as plain text.\n    '
    data = {
        'doc': None,
        'plainexamples': None,
        'returndocs': None,
        'metadata': None,
    }
    string_to_vars = {
        'DOCUMENTATION': 'doc',
        'EXAMPLES': 'plainexamples',
        'RETURN': 'returndocs',
        'ANSIBLE_METADATA': 'metadata',
    }
    try:
        M = ast.parse(''.join(open(filename)))
        try:
            display.debug('Attempt first docstring is yaml docs')
            docstring = yaml.load(M.body[0].value.s)
            for string in string_to_vars.keys():
                if (string in docstring):
                    data[string_to_vars[string]] = docstring[string]
                display.debug(('assigned :%s' % string_to_vars[string]))
        except Exception as e:
            display.debug(('failed docstring parsing: %s' % str(e)))
        if (('docs' not in data) or (not data['docs'])):
            display.debug('Fallback to vars parsing')
            for child in M.body:
                if isinstance(child, ast.Assign):
                    for t in child.targets:
                        try:
                            theid = t.id
                        except AttributeError:
                            display.warning(('Failed to assign id for %s on %s, skipping' % (t, filename)))
                            continue
                        if (theid in string_to_vars):
                            varkey = string_to_vars[theid]
                            if isinstance(child.value, ast.Dict):
                                data[varkey] = ast.literal_eval(child.value)
                            elif (theid in ['DOCUMENTATION', 'ANSIBLE_METADATA']):
                                data[varkey] = AnsibleLoader(child.value.s, file_name=filename).get_single_data()
                            else:
                                data[varkey] = child.value.s
                            display.debug(('assigned :%s' % varkey))
    except:
        if verbose:
            display.error(('unable to parse %s' % filename))
        if (not ignore_errors):
            raise
    return data