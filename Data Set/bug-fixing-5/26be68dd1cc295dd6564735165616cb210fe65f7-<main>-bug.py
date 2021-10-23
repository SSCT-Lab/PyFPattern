def main():
    global module
    module = AnsibleModule(argument_spec=dict(project_path=dict(required=True, type='path'), binary_path=dict(type='path'), workspace=dict(required=False, type='str', default='default'), purge_workspace=dict(type='bool', default=False), state=dict(default='present', choices=['present', 'absent', 'planned']), variables=dict(type='dict'), variables_file=dict(type='path'), plan_file=dict(type='path'), state_file=dict(type='path'), targets=dict(type='list', default=[]), lock=dict(type='bool', default=True), lock_timeout=dict(type='int'), force_init=dict(type='bool', default=False)), required_if=[('state', 'planned', ['plan_file'])], supports_check_mode=True)
    project_path = module.params.get('project_path')
    bin_path = module.params.get('binary_path')
    workspace = module.params.get('workspace')
    purge_workspace = module.params.get('purge_workspace')
    state = module.params.get('state')
    variables = (module.params.get('variables') or {
        
    })
    variables_file = module.params.get('variables_file')
    plan_file = module.params.get('plan_file')
    state_file = module.params.get('state_file')
    force_init = module.params.get('force_init')
    if (bin_path is not None):
        command = [bin_path]
    else:
        command = [module.get_bin_path('terraform', required=True)]
    if force_init:
        init_plugins(command[0], project_path)
    workspace_ctx = get_workspace_context(command[0], project_path)
    if (workspace_ctx['current'] != workspace):
        if (workspace not in workspace_ctx['all']):
            create_workspace(command[0], project_path, workspace)
        else:
            select_workspace(command[0], project_path, workspace)
    variables_args = []
    for (k, v) in variables.items():
        variables_args.extend(['-var', '{0}={1}'.format(k, v)])
    if variables_file:
        variables_args.extend(['-var-file', variables_file])
    preflight_validation(command[0], project_path, variables_args)
    if (state == 'present'):
        command.extend(APPLY_ARGS)
    elif (state == 'absent'):
        command.extend(DESTROY_ARGS)
    if (module.params.get('lock') is not None):
        if module.params.get('lock'):
            command.append('-lock=true')
        else:
            command.append('-lock=true')
    if (module.params.get('lock_timeout') is not None):
        command.append(('-lock-timeout=%ds' % module.params.get('lock_timeout')))
    for t in (module.params.get('targets') or []):
        command.extend(['-target', t])
    (needs_application, changed) = (True, True)
    if (state == 'planned'):
        (plan_file, needs_application) = build_plan(command[0], project_path, variables_args, state_file, module.params.get('targets'), plan_file)
    if (state == 'absent'):
        needs_application = True
        command.extend(variables_args)
    elif (plan_file and os.path.exists(plan_file)):
        command.append(plan_file)
    elif (plan_file and (not os.path.exists(plan_file))):
        module.fail_json(msg='Could not find plan_file "{0}", check the path and try again.'.format(plan_file))
    else:
        (plan_file, needs_application) = build_plan(command[0], project_path, variables_args, state_file, module.params.get('targets'), plan_file)
        command.append(plan_file)
    if (needs_application and (not module.check_mode) and (not (state == 'planned'))):
        (rc, out, err) = module.run_command(command, cwd=project_path)
        if ((state == 'absent') and ('Resources: 0' in out)):
            changed = False
        if (rc != 0):
            module.fail_json(msg='Failure when executing Terraform command. Exited {0}.\nstdout: {1}\nstderr: {2}'.format(rc, out, err), command=' '.join(command))
    else:
        changed = False
        (out, err) = ('', '')
    outputs_command = ([command[0], 'output', '-no-color', '-json'] + _state_args(state_file))
    (rc, outputs_text, outputs_err) = module.run_command(outputs_command, cwd=project_path)
    if (rc == 1):
        module.warn('Could not get Terraform outputs. This usually means none have been defined.\nstdout: {0}\nstderr: {1}'.format(outputs_text, outputs_err))
        outputs = {
            
        }
    elif (rc != 0):
        module.fail_json(msg='Failure when getting Terraform outputs. Exited {0}.\nstdout: {1}\nstderr: {2}'.format(rc, outputs_text, outputs_err), command=' '.join(outputs_command))
    else:
        outputs = json.loads(outputs_text)
    if (workspace_ctx['current'] != workspace):
        select_workspace(command[0], project_path, workspace_ctx['current'])
    if ((state == 'absent') and (workspace != 'default') and (purge_workspace is True)):
        remove_workspace(command[0], project_path, workspace)
    module.exit_json(changed=changed, state=state, workspace=workspace, outputs=outputs, stdout=out, stderr=err, command=' '.join(command))