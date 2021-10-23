def find_retention_policy(module, client):
    database_name = module.params['database_name']
    policy_name = module.params['policy_name']
    retention_policy = None
    try:
        retention_policies = client.get_list_retention_policies(database=database_name)
        for policy in retention_policies:
            if (policy['name'] == policy_name):
                retention_policy = policy
                break
    except requests.exceptions.ConnectionError as e:
        module.fail_json(msg=str(e))
    return retention_policy