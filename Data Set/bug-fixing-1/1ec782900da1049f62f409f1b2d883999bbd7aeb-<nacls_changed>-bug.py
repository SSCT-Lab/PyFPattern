

def nacls_changed(nacl, client, module):
    changed = False
    params = dict()
    params['egress'] = module.params.get('egress')
    params['ingress'] = module.params.get('ingress')
    nacl_id = nacl['NetworkAcls'][0]['NetworkAclId']
    nacl = describe_network_acl(client, module)
    entries = nacl['NetworkAcls'][0]['Entries']
    tmp_egress = [entry for entry in entries if ((entry['Egress'] is True) and (DEFAULT_EGRESS != entry))]
    tmp_ingress = [entry for entry in entries if (entry['Egress'] is False)]
    egress = [rule for rule in tmp_egress if (DEFAULT_EGRESS != rule)]
    ingress = [rule for rule in tmp_ingress if (DEFAULT_INGRESS != rule)]
    if rules_changed(egress, params['egress'], True, nacl_id, client, module):
        changed = True
    if rules_changed(ingress, params['ingress'], False, nacl_id, client, module):
        changed = True
    return changed
