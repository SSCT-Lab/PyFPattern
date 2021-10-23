def process_plugins(module_map, templates, outputname, output_dir, ansible_version, plugin_type):
    for (module_index, module) in enumerate(module_map):
        show_progress(module_index)
        fname = module_map[module]['path']
        display.vvvvv(pp.pformat(('process_plugins info: ', module_map[module])))
        if (module_map[module]['doc'] is None):
            display.error(('%s MISSING DOCUMENTATION' % (fname,)))
            _doc = {
                plugin_type: module,
                'version_added': '2.4',
                'filename': fname,
            }
            module_map[module]['doc'] = _doc
        doc = module_map[module]['doc']
        display.vvvvv(pp.pformat(('process_plugins doc: ', doc)))
        doc['module'] = doc.get('module', module)
        doc['version_added'] = doc.get('version_added', 'historical')
        doc['plugin_type'] = plugin_type
        if (module_map[module]['deprecated'] and ('deprecated' not in doc)):
            display.warning(('%s PLUGIN MISSING DEPRECATION DOCUMENTATION: %s' % (fname, 'deprecated')))
        required_fields = ('short_description',)
        for field in required_fields:
            if (field not in doc):
                display.warning(("%s PLUGIN MISSING field '%s'" % (fname, field)))
        not_nullable_fields = ('short_description',)
        for field in not_nullable_fields:
            if ((field in doc) and (doc[field] in (None, ''))):
                print(("%s: WARNING: MODULE field '%s' DOCUMENTATION is null/empty value=%s" % (fname, field, doc[field])))
        if ('description' in doc):
            if isinstance(doc['description'], string_types):
                doc['description'] = [doc['description']]
            elif (not isinstance(doc['description'], (list, tuple))):
                raise AnsibleError(('Description must be a string or list of strings.  Got %s' % type(doc['description'])))
        else:
            doc['description'] = []
        if ('version_added' not in doc):
            raise AnsibleError(('*** ERROR: missing version_added in: %s ***\n' % module))
        if module_map[module]['aliases']:
            doc['aliases'] = module_map[module]['aliases']
        added = 0
        if (doc['version_added'] == 'historical'):
            del doc['version_added']
        else:
            added = doc['version_added']
        if too_old(added):
            del doc['version_added']
        option_names = []
        if (('options' in doc) and doc['options']):
            for (k, v) in iteritems(doc['options']):
                if ('description' not in doc['options'][k]):
                    raise AnsibleError(("Missing required description for parameter '%s' in '%s' " % (k, module)))
                if isinstance(doc['options'][k]['description'], string_types):
                    doc['options'][k]['description'] = [doc['options'][k]['description']]
                elif (not isinstance(doc['options'][k]['description'], (list, tuple))):
                    raise AnsibleError(("Invalid type for options['%s']['description']. Must be string or list of strings.  Got %s" % (k, type(doc['options'][k]['description']))))
                required_value = doc['options'][k].get('required', False)
                if (not isinstance(required_value, bool)):
                    raise AnsibleError(("Invalid required value '%s' for parameter '%s' in '%s' (must be truthy)" % (required_value, k, module)))
                if (('version_added' in doc['options'][k]) and too_old(doc['options'][k]['version_added'])):
                    del doc['options'][k]['version_added']
                option_names.append(k)
        option_names.sort()
        doc['option_keys'] = option_names
        doc['filename'] = fname
        doc['source'] = module_map[module]['source']
        doc['docuri'] = doc['module'].replace('_', '-')
        doc['now_date'] = datetime.date.today().strftime('%Y-%m-%d')
        doc['ansible_version'] = ansible_version
        if isinstance(module_map[module]['examples'], string_types):
            doc['plainexamples'] = module_map[module]['examples']
        else:
            doc['plainexamples'] = ''
        doc['metadata'] = module_map[module]['metadata']
        display.vvvvv(pp.pformat(module_map[module]))
        if module_map[module]['returndocs']:
            try:
                doc['returndocs'] = yaml.safe_load(module_map[module]['returndocs'])
            except Exception as e:
                print(('%s:%s:yaml error:%s:returndocs=%s' % (fname, module, e, module_map[module]['returndocs'])))
                doc['returndocs'] = None
        else:
            doc['returndocs'] = None
        doc['author'] = doc.get('author', ['UNKNOWN'])
        if isinstance(doc['author'], string_types):
            doc['author'] = [doc['author']]
        display.v(('about to template %s' % module))
        display.vvvvv(pp.pformat(doc))
        try:
            text = templates['plugin'].render(doc)
        except Exception as e:
            display.warning(msg=('Could not parse %s due to %s' % (module, e)))
            continue
        if (LooseVersion(jinja2.__version__) < LooseVersion('2.10')):
            text = re.sub(' +\n', '\n', text)
        write_data(text, output_dir, outputname, module)
        if module_map[module]['aliases']:
            for alias in module_map[module]['aliases']:
                if (alias in module_map[module]['aliases_deprecated']):
                    doc['alias'] = alias
                    display.v(('about to template %s (deprecation alias %s)' % (module, alias)))
                    display.vvvvv(pp.pformat(doc))
                    try:
                        text = templates['plugin_deprecation_stub'].render(doc)
                    except Exception as e:
                        display.warning(msg=('Could not parse %s (deprecation alias %s) due to %s' % (module, alias, e)))
                        continue
                    if (LooseVersion(jinja2.__version__) < LooseVersion('2.10')):
                        text = re.sub(' +\n', '\n', text)
                    write_data(text, output_dir, outputname, alias)