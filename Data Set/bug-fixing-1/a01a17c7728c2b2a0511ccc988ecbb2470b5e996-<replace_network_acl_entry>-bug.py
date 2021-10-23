

def replace_network_acl_entry(entries, Egress, nacl_id, client, module):
    params = dict()
    for entry in entries:
        params = entry
        params['NetworkAclId'] = nacl_id
        try:
            if (not module.check_mode):
                client.replace_network_acl_entry(**params)
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=str(e))
