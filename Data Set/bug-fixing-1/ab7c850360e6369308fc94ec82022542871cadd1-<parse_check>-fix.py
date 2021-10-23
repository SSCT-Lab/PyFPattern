

def parse_check(module):
    if (len([p for p in (module.params.get('script'), module.params.get('ttl'), module.params.get('http')) if p]) > 1):
        module.fail_json(msg='checks are either script, http or ttl driven, supplying more than one does not make sense')
    if (module.params.get('check_id') or module.params.get('script') or module.params.get('ttl') or module.params.get('http')):
        return ConsulCheck(module.params.get('check_id'), module.params.get('check_name'), module.params.get('check_node'), module.params.get('check_host'), module.params.get('script'), module.params.get('interval'), module.params.get('ttl'), module.params.get('notes'), module.params.get('http'), module.params.get('timeout'), module.params.get('service_id'))
