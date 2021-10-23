

def get_policy_statement(module, client):
    'Checks that policy exists and if so, that statement ID is present or absent.\n\n    :param module:\n    :param client:\n    :return:\n    '
    sid = module.params['statement_id']
    api_params = set_api_params(module, ('function_name',))
    qualifier = get_qualifier(module)
    if qualifier:
        api_params.update(Qualifier=qualifier)
    policy_results = None
    try:
        policy_results = client.get_policy(**api_params)
    except ClientError as e:
        try:
            if (e.response['Error']['Code'] == 'ResourceNotFoundException'):
                return {
                    
                }
        except AttributeError:
            pass
        module.fail_json_aws(e, msg='retrieving function policy')
    except Exception as e:
        module.fail_json_aws(e, msg='retrieving function policy')
    policy = json.loads(policy_results.get('Policy', '{}'))
    return extract_statement(policy, sid)
