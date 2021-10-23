def build_plan(bin_path, project_path, variables_args, state_file, targets, plan_path=None):
    if (plan_path is None):
        (f, plan_path) = tempfile.mkstemp(suffix='.tfplan')
    command = [bin_path, 'plan', '-input=false', '-no-color', '-detailed-exitcode', '-out', plan_path]
    for t in (module.params.get('targets') or []):
        command.extend(['-target', t])
    command.extend(_state_args(state_file))
    (rc, out, err) = module.run_command((command + variables_args), cwd=project_path)
    if (rc == 0):
        return (plan_path, False)
    elif (rc == 1):
        module.fail_json(msg='Terraform plan could not be created\r\nSTDOUT: {0}\r\n\r\nSTDERR: {1}'.format(out, err))
    elif (rc == 2):
        return (plan_path, True)
    module.fail_json(msg='Terraform plan failed with unexpected exit code {0}. \r\nSTDOUT: {1}\r\n\r\nSTDERR: {2}'.format(rc, out, err))