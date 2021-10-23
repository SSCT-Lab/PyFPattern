

def parse_cli(output, tmpl):
    try:
        template = Template()
    except ImportError as exc:
        raise AnsibleError(str(exc))
    spec = yaml.load(open(tmpl).read())
    obj = {
        
    }
    for (name, attrs) in iteritems(spec['keys']):
        value = attrs['value']
        if template.can_template(value):
            variables = spec.get('vars', {
                
            })
            value = template(value, variables)
        if (('start_block' in attrs) and ('end_block' in attrs)):
            start_block = re.compile(attrs['start_block'])
            end_block = re.compile(attrs['end_block'])
            blocks = list()
            lines = None
            block_started = False
            for line in output.split('\n'):
                match_start = start_block.match(line)
                match_end = end_block.match(line)
                if match_start:
                    if lines:
                        blocks.append('\n'.join(lines))
                    lines = list()
                    lines.append(line)
                    block_started = True
                elif match_end:
                    if lines:
                        lines.append(line)
                    block_started = False
                elif block_started:
                    if lines:
                        lines.append(line)
            regex_items = [re.compile(r) for r in attrs['items']]
            objects = list()
            for block in blocks:
                if (isinstance(value, Mapping) and ('key' not in value)):
                    items = list()
                    for regex in regex_items:
                        match = regex.search(block)
                        if match:
                            item_values = match.groupdict()
                            item_values['match'] = list(match.groups())
                            items.append(item_values)
                        else:
                            items.append(None)
                    objects.append(dict([(k, template(v, {
                        'item': items,
                    })) for (k, v) in iteritems(value)]))
                elif isinstance(value, Mapping):
                    items = list()
                    for regex in regex_items:
                        match = regex.search(block)
                        if match:
                            item_values = match.groupdict()
                            item_values['match'] = list(match.groups())
                            items.append(item_values)
                        else:
                            items.append(None)
                    key = template(value['key'], {
                        'item': items,
                    })
                    values = dict([(k, template(v, {
                        'item': items,
                    })) for (k, v) in iteritems(value['values'])])
                    objects.append({
                        key: values,
                    })
            return objects
        elif ('items' in attrs):
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
