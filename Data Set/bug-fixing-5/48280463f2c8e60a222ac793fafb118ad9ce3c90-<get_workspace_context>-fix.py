def get_workspace_context(bin_path, project_path):
    workspace_ctx = {
        'current': 'default',
        'all': [],
    }
    command = [bin_path, 'workspace', 'list', '-no-color']
    (rc, out, err) = module.run_command(command, cwd=project_path)
    if (rc != 0):
        module.fail_json(msg='Failed to list Terraform workspaces:\r\n{0}'.format(err))
    for item in out.split('\n'):
        stripped_item = item.strip()
        if (not stripped_item):
            continue
        elif stripped_item.startswith('* '):
            workspace_ctx['current'] = stripped_item.replace('* ', '')
        else:
            workspace_ctx['all'].append(stripped_item)
    return workspace_ctx