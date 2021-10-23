

def create_changeset(module, stack_params, cfn):
    if (('TemplateBody' not in stack_params) and ('TemplateURL' not in stack_params)):
        module.fail_json(msg="Either 'template' or 'template_url' is required.")
    try:
        if (not ('ChangeSetName' in stack_params)):
            json_params = json.dumps(stack_params, sort_keys=True)
            changeset_name = ((('Ansible-' + stack_params['StackName']) + '-') + sha1(to_bytes(json_params, errors='surrogate_or_strict')).hexdigest())
            stack_params['ChangeSetName'] = changeset_name
        pending_changesets = list_changesets(cfn, stack_params['StackName'])
        if (changeset_name in pending_changesets):
            warning = (('WARNING: ' + str(len(pending_changesets))) + ' pending changeset(s) exist(s) for this stack!')
            result = dict(changed=False, output=(('ChangeSet ' + changeset_name) + ' already exists.'), warnings=[warning])
        else:
            cs = cfn.create_change_set(**stack_params)
            result = stack_operation(cfn, stack_params['StackName'], 'UPDATE')
            result['warnings'] = [((('Created changeset named ' + changeset_name) + ' for stack ') + stack_params['StackName']), ('You can execute it using: aws cloudformation execute-change-set --change-set-name ' + cs['Id']), 'NOTE that dependencies on this stack might fail due to pending changes!']
    except Exception as err:
        error_msg = boto_exception(err)
        if ('No updates are to be performed.' in error_msg):
            result = dict(changed=False, output='Stack is already up-to-date.')
        else:
            module.fail_json(msg='Failed to create change set: {0}'.format(error_msg), exception=traceback.format_exc())
    if (not result):
        module.fail_json(msg='empty result')
    return result
