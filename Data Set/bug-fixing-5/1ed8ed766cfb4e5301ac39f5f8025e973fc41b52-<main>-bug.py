def main():
    module = AnsibleModule(argument_spec=dict(host=dict(type='str', required=True), login=dict(type='str', default='Administrator'), password=dict(type='str', default='admin', no_log=True), ssl_version=dict(type='str', default='TLSv1', choices=['SSLv3', 'SSLv23', 'TLSv1', 'TLSv1_1', 'TLSv1_2'])), supports_check_mode=True)
    if (not HAS_HPILO):
        module.fail_json(msg=missing_required_lib('python-hpilo'), exception=HPILO_IMP_ERR)
    host = module.params['host']
    login = module.params['login']
    password = module.params['password']
    ssl_version = getattr(hpilo.ssl, ('PROTOCOL_' + module.params.get('ssl_version').upper().replace('V', 'v')))
    ilo = hpilo.Ilo(host, login=login, password=password, ssl_version=ssl_version)
    facts = {
        'module_hw': True,
    }
    data = ilo.get_host_data()
    for entry in data:
        if ('type' not in entry):
            continue
        elif (entry['type'] == 0):
            facts['hw_bios_version'] = entry['Family']
            facts['hw_bios_date'] = entry['Date']
        elif (entry['type'] == 1):
            facts['hw_uuid'] = entry['UUID']
            facts['hw_system_serial'] = entry['Serial Number'].rstrip()
            facts['hw_product_name'] = entry['Product Name']
            facts['hw_product_uuid'] = entry['cUUID']
        elif (entry['type'] == 209):
            if ('fields' in entry):
                for (name, value) in [(e['name'], e['value']) for e in entry['fields']]:
                    if name.startswith('Port'):
                        try:
                            factname = ('hw_eth' + str((int(value) - 1)))
                        except Exception:
                            factname = 'hw_eth_ilo'
                    elif name.startswith('MAC'):
                        facts[factname] = {
                            'macaddress': value.replace('-', ':'),
                            'macaddress_dash': value,
                        }
            else:
                (factname, entry_facts) = parse_flat_interface(entry, 'hw_eth_ilo')
                facts[factname] = entry_facts
        elif (entry['type'] == 209):
            for (name, value) in [(e['name'], e['value']) for e in entry['fields']]:
                if name.startswith('Port'):
                    try:
                        factname = ('hw_iscsi' + str((int(value) - 1)))
                    except Exception:
                        factname = 'hw_iscsi_ilo'
                elif name.startswith('MAC'):
                    facts[factname] = {
                        'macaddress': value.replace('-', ':'),
                        'macaddress_dash': value,
                    }
        elif (entry['type'] == 233):
            (factname, entry_facts) = parse_flat_interface(entry, 'hw_eth_ilo')
            facts[factname] = entry_facts
    health = ilo.get_embedded_health()
    facts['hw_health'] = health
    memory_details_summary = health.get('memory', {
        
    }).get('memory_details_summary')
    if memory_details_summary:
        facts['hw_memory_details_summary'] = memory_details_summary
        facts['hw_memory_total'] = 0
        for (cpu, details) in memory_details_summary.items():
            cpu_total_memory_size = details.get('total_memory_size')
            if cpu_total_memory_size:
                ram = re.search('(\\d+)\\s+(\\w+)', cpu_total_memory_size)
                if ram:
                    if (ram.group(2) == 'GB'):
                        facts['hw_memory_total'] = (facts['hw_memory_total'] + int(ram.group(1)))
        facts['hw_memory_total'] = '{0} GB'.format(facts['hw_memory_total'])
    module.exit_json(ansible_facts=facts)