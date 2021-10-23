

def create_changeset(module, stack_params, cfn, events_limit):
    if (('TemplateBody' not in stack_params) and ('TemplateURL' not in stack_params)):
        module.fail_json(msg="Either 'template' or 'template_url' is required.")
    if (module.params['changeset_name'] is not None):
        stack_params['ChangeSetName'] = module.params['changeset_name']
    stack_params.pop('ClientRequestToken', None)
    try:
        changeset_name = build_changeset_name(stack_params)
        stack_params['ChangeSetName'] = changeset_name
        pending_changesets = list_changesets(cfn, stack_params['StackName'])
        if (changeset_name in pending_changesets):
            warning = ('WARNING: %d pending changeset(s) exist(s) for this stack!' % len(pending_changesets))
            result = dict(changed=False, output=('ChangeSet %s already exists.' % changeset_name), warnings=[warning])
        else:
            cs = cfn.create_change_set(**stack_params)
            time_end = (time.time() + 600)
            while (time.time() < time_end):
                try:
                    newcs = cfn.describe_change_set(ChangeSetName=cs['Id'])
                except botocore.exceptions.BotoCoreError as err:
                    error_msg = boto_exception(err)
                    module.fail_json(msg=error_msg)
                if ((newcs['Status'] == 'CREATE_PENDING') or (newcs['Status'] == 'CREATE_IN_PROGRESS')):
                    time.sleep(1)
                elif ((newcs['Status'] == 'FAILED') and ("The submitted information didn't contain changes" in newcs['StatusReason'])):
                    cfn.delete_change_set(ChangeSetName=cs['Id'])
                    result = dict(changed=False, output='Stack is already up-to-date, Change Set refused to create due to lack of changes.')
                    module.exit_json(**result)
                else:
                    break
                time.sleep(1)
            result = stack_operation(cfn, stack_params['StackName'], 'CREATE_CHANGESET', events_limit)
            result['warnings'] = [('Created changeset named %s for stack %s' % (changeset_name, stack_params['StackName'])), ('You can execute it using: aws cloudformation execute-change-set --change-set-name %s' % cs['Id']), 'NOTE that dependencies on this stack might fail due to pending changes!']
    except Exception as err:
        error_msg = boto_exception(err)
        if ('No updates are to be performed.' in error_msg):
            result = dict(changed=False, output='Stack is already up-to-date.')
        else:
            module.fail_json(msg='Failed to create change set: {0}'.format(error_msg), exception=traceback.format_exc())
    if (not result):
        module.fail_json(msg='empty result')
    return result
