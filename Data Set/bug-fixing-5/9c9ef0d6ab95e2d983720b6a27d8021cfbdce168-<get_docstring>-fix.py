def get_docstring(filename, verbose=False):
    '\n    Search for assignment of the DOCUMENTATION and EXAMPLES variables\n    in the given file.\n    Parse DOCUMENTATION from YAML and return the YAML doc or None\n    together with EXAMPLES, as plain text.\n\n    DOCUMENTATION can be extended using documentation fragments\n    loaded by the PluginLoader from the module_docs_fragments\n    directory.\n    '
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
        if data['doc']:
            add_fragments(data['doc'], filename)
        if data['metadata']:
            for x in ('version', 'metadata_version'):
                if (x in data['metadata']):
                    del data['metadata'][x]
    except:
        display.error(('unable to parse %s' % filename))
        if (verbose is True):
            display.display(('unable to parse %s' % filename))
            raise
    return (data['doc'], data['plainexamples'], data['returndocs'], data['metadata'])