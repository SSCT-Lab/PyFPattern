def _workspace_cmd(bin_path, project_path, action, workspace):
    command = [bin_path, 'workspace', action, workspace]
    (rc, out, err) = module.run_command(command, cwd=project_path)
    if (rc != 0):
        module.fail_json(msg='Failed to {0} workspace:\r\n{1}'.format(action, err))
    return (rc, out, err)