

def check_declarative_intent_params(want, module):
    if module.params['interfaces']:
        time.sleep(module.params['delay'])
        have = map_config_to_obj(module)
        for w in want:
            for i in w['interfaces']:
                obj_in_have = search_obj_in_list(w['name'], have)
                if (obj_in_have and (i not in obj_in_have.get('interfaces', []))):
                    module.fail_json(msg=('Interface %s not configured on vrf %s' % (i, w['name'])))
