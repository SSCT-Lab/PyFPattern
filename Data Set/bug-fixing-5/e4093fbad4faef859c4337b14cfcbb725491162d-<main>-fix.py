def main():
    argument_spec = mso_argument_spec()
    argument_spec.update(schema=dict(type='str', required=True), template=dict(type='str', required=True), filter=dict(type='str', required=True), filter_display_name=dict(type='str'), entry=dict(type='str', aliases=['name']), description=dict(type='str', aliases=['entry_description']), display_name=dict(type='str', aliases=['entry_display_name']), ethertype=dict(type='str', choices=['arp', 'fcoe', 'ip', 'ipv4', 'ipv6', 'mac-security', 'mpls-unicast', 'trill', 'unspecified']), ip_protocol=dict(type='str', choices=['eigrp', 'egp', 'icmp', 'icmpv6', 'igmp', 'igp', 'l2tp', 'ospfigp', 'pim', 'tcp', 'udp', 'unspecified']), tcp_session_rules=dict(type='list', choices=['acknowledgement', 'established', 'finish', 'synchronize', 'reset', 'unspecified']), source_from=dict(type='str'), source_to=dict(type='str'), destination_from=dict(type='str'), destination_to=dict(type='str'), arp_flag=dict(type='str', choices=['reply', 'request', 'unspecified']), stateful=dict(type='bool'), fragments_only=dict(type='bool'), state=dict(type='str', default='present', choices=['absent', 'present', 'query']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'absent', ['entry']], ['state', 'present', ['entry']]])
    schema = module.params['schema']
    template = module.params['template']
    filter_name = module.params['filter']
    filter_display_name = module.params['filter_display_name']
    entry = module.params['entry']
    display_name = module.params['display_name']
    description = module.params['description']
    ethertype = module.params['ethertype']
    ip_protocol = module.params['ip_protocol']
    tcp_session_rules = module.params['tcp_session_rules']
    source_from = module.params['source_from']
    source_to = module.params['source_to']
    destination_from = module.params['destination_from']
    destination_to = module.params['destination_to']
    arp_flag = module.params['arp_flag']
    stateful = module.params['stateful']
    fragments_only = module.params['fragments_only']
    state = module.params['state']
    mso = MSOModule(module)
    schema_obj = mso.get_obj('schemas', displayName=schema)
    if (not schema_obj):
        mso.fail_json(msg="Provided schema '{0}' does not exist".format(schema))
    schema_path = 'schemas/{id}'.format(**schema_obj)
    templates = [t['name'] for t in schema_obj['templates']]
    if (template not in templates):
        mso.fail_json(msg="Provided template '{template}' does not exist. Existing templates: {templates}".format(template=template, templates=', '.join(templates)))
    template_idx = templates.index(template)
    mso.existing = {
        
    }
    filter_idx = None
    entry_idx = None
    filters = [f['name'] for f in schema_obj['templates'][template_idx]['filters']]
    if (filter_name in filters):
        filter_idx = filters.index(filter_name)
        entries = [f['name'] for f in schema_obj['templates'][template_idx]['filters'][filter_idx]['entries']]
        if (entry in entries):
            entry_idx = entries.index(entry)
            mso.existing = schema_obj['templates'][template_idx]['filters'][filter_idx]['entries'][entry_idx]
    if (state == 'query'):
        if (entry is None):
            if (filter_idx is None):
                mso.fail_json(msg="Filter '{filter}' not found".format(filter=filter_name))
            mso.existing = schema_obj['templates'][template_idx]['filters'][filter_idx]['entries']
        elif (not mso.existing):
            mso.fail_json(msg="Entry '{entry}' not found".format(entry=entry))
        mso.exit_json()
    filters_path = '/templates/{0}/filters'.format(template)
    filter_path = '/templates/{0}/filters/{1}'.format(template, filter_name)
    entries_path = '/templates/{0}/filters/{1}/entries'.format(template, filter_name)
    entry_path = '/templates/{0}/filters/{1}/entries/{2}'.format(template, filter_name, entry)
    ops = []
    mso.previous = mso.existing
    if (state == 'absent'):
        mso.proposed = mso.sent = {
            
        }
        if (filter_idx is None):
            pass
        elif (entry_idx is None):
            pass
        elif (len(entries) == 1):
            mso.existing = {
                
            }
            ops.append(dict(op='remove', path=filter_path))
        else:
            mso.existing = {
                
            }
            ops.append(dict(op='remove', path=entry_path))
    elif (state == 'present'):
        if (not mso.existing):
            if (display_name is None):
                display_name = entry
            if (description is None):
                description = ''
            if (ethertype is None):
                ethertype = 'unspecified'
            if (ip_protocol is None):
                ip_protocol = 'unspecified'
            if (tcp_session_rules is None):
                tcp_session_rules = ['unspecified']
            if (source_from is None):
                source_from = 'unspecified'
            if (source_to is None):
                source_to = 'unspecified'
            if (destination_from is None):
                destination_from = 'unspecified'
            if (destination_to is None):
                destination_to = 'unspecified'
            if (arp_flag is None):
                arp_flag = 'unspecified'
            if (stateful is None):
                stateful = False
            if (fragments_only is None):
                fragments_only = False
        payload = dict(name=entry, displayName=display_name, description=description, etherType=ethertype, ipProtocol=ip_protocol, tcpSessionRules=tcp_session_rules, sourceFrom=source_from, sourceTo=source_to, destinationFrom=destination_from, destinationTo=destination_to, arpFlag=arp_flag, stateful=stateful, matchOnlyFragments=fragments_only)
        mso.sanitize(payload, collate=True)
        if (filter_idx is None):
            if (filter_display_name is None):
                filter_display_name = filter_name
            payload = dict(name=filter_name, displayName=filter_display_name, entries=[mso.sent])
            ops.append(dict(op='add', path=(filters_path + '/-'), value=payload))
        elif (entry_idx is None):
            ops.append(dict(op='add', path=(entries_path + '/-'), value=mso.sent))
        else:
            for (key, value) in mso.sent.items():
                ops.append(dict(op='replace', path=((entry_path + '/') + key), value=value))
        mso.existing = mso.proposed
    if (not module.check_mode):
        mso.request(schema_path, method='PATCH', data=ops)
    mso.exit_json()