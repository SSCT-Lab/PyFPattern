def parse_cli(output, tmpl):
    try:
        template = Template()
    except ImportError as exc:
        raise AnsibleError(str(exc))
    spec = yaml.load(open(tmpl).read())
    obj = {
        
    }
    for (name, attrs) in iteritems(spec['attributes']):
        value = attrs['value']
        if template.can_template(value):
            value = template(value, spec)
        if ('items' in attrs):
            regexp = re.compile(attrs['items'])
            when = attrs.get('when')
            conditional = ('{%% if %s %%}True{%% else %%}False{%% endif %%}' % when)
            if (isinstance(value, Mapping) and ('key' not in value)):
                values = list()
                for item in re_matchall(regexp, output):
                    entry = {
                        
                    }
                    for (item_key, item_value) in iteritems(value):
                        entry[item_key] = template(item_value, {
                            'item': item,
                        })
                    if when:
                        if template(conditional, {
                            'item': entry,
                        }):
                            values.append(entry)
                    else:
                        values.append(entry)
                obj[name] = values
            elif isinstance(value, Mapping):
                values = dict()
                for item in re_matchall(regexp, output):
                    entry = {
                        
                    }
                    for (item_key, item_value) in iteritems(value['values']):
                        entry[item_key] = template(item_value, {
                            'item': item,
                        })
                    key = template(value['key'], {
                        'item': item,
                    })
                    if when:
                        if template(conditional, {
                            'item': {
                                'key': key,
                                'value': entry,
                            },
                        }):
                            values[key] = entry
                    else:
                        values[key] = entry
                obj[name] = values
            else:
                item = re_search(regexp, output)
                obj[name] = template(value, {
                    'item': item,
                })
        else:
            obj[name] = value
    return obj