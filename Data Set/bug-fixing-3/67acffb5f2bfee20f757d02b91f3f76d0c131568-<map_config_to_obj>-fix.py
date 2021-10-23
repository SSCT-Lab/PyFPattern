def map_config_to_obj(module):
    config = get_config(module)
    return {
        'hostname': parse_hostname(config),
        'domain_name': parse_domain_name(config),
        'domain_search': parse_domain_search(config),
        'lookup_source': parse_lookup_source(config),
        'lookup_enabled': (('no ip domain lookup' not in config) and ('no ip domain-lookup' not in config)),
        'name_servers': parse_name_servers(config),
    }