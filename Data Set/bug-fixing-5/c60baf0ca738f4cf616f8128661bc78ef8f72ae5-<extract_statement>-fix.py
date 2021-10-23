def extract_statement(policy, sid):
    'return flattened single policy statement from a policy\n\n    If a policy statement is present in the policy extract it and\n    return it in a flattened form.  Otherwise return an empty\n    dictionary.\n    '
    if ('Statement' not in policy):
        return {
            
        }
    policy_statement = {
        
    }
    for statement in policy['Statement']:
        if (statement['Sid'] == sid):
            policy_statement['action'] = statement['Action']
            try:
                policy_statement['principal'] = statement['Principal']['Service']
            except KeyError:
                pass
            try:
                policy_statement['principal'] = statement['Principal']['AWS']
            except KeyError:
                pass
            try:
                policy_statement['source_arn'] = statement['Condition']['ArnLike']['AWS:SourceArn']
            except KeyError:
                pass
            try:
                policy_statement['source_account'] = statement['Condition']['StringEquals']['AWS:SourceAccount']
            except KeyError:
                pass
            try:
                policy_statement['event_source_token'] = statement['Condition']['StringEquals']['lambda:EventSourceToken']
            except KeyError:
                pass
            break
    return policy_statement