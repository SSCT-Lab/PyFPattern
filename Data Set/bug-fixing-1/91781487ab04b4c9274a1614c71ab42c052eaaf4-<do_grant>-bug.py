

def do_grant(kms, keyarn, role_arn, granttypes, mode='grant', dry_run=True, clean_invalid_entries=True):
    ret = {
        
    }
    keyret = kms.get_key_policy(KeyId=keyarn, PolicyName='default')
    policy = json.loads(keyret['Policy'])
    changes_needed = {
        
    }
    assert_policy_shape(policy)
    had_invalid_entries = False
    for statement in policy['Statement']:
        for granttype in ['role', 'role grant', 'admin']:
            if ((mode == 'grant') and (statement['Sid'] == statement_label[granttype])):
                if (granttype in granttypes):
                    invalid_entries = list(filter((lambda x: (not x.startswith('arn:aws:iam::'))), statement['Principal']['AWS']))
                    if (clean_invalid_entries and len(list(invalid_entries))):
                        valid_entries = filter((lambda x: x.startswith('arn:aws:iam::')), statement['Principal']['AWS'])
                        statement['Principal']['AWS'] = valid_entries
                        had_invalid_entries = True
                    if (not (role_arn in statement['Principal']['AWS'])):
                        changes_needed[granttype] = 'add'
                        if (not dry_run):
                            statement['Principal']['AWS'].append(role_arn)
                elif (role_arn in statement['Principal']['AWS']):
                    changes_needed[granttype] = 'remove'
                    if (not dry_run):
                        statement['Principal']['AWS'].remove(role_arn)
            elif ((mode == 'deny') and (statement['Sid'] == statement_label[granttype]) and (role_arn in statement['Principal']['AWS'])):
                changes_needed[granttype] = 'remove'
                if (not dry_run):
                    statement['Principal']['AWS'].remove(role_arn)
    try:
        if (len(changes_needed) and (not dry_run)):
            policy_json_string = json.dumps(policy)
            kms.put_key_policy(KeyId=keyarn, PolicyName='default', Policy=policy_json_string)
    except:
        raise Exception('{}: // {}'.format('e', policy_json_string))
        ret['changed'] = True
    ret['changes_needed'] = changes_needed
    ret['had_invalid_entries'] = had_invalid_entries
    if dry_run:
        ret['changed'] = (not (len(changes_needed) == 0))
    return ret
