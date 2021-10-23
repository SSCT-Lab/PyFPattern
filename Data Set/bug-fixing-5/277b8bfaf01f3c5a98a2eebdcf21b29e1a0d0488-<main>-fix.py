def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True), path=dict(required=True, type='path'), link=dict(required=False, type='path'), priority=dict(required=False, type='int', default=50)), supports_check_mode=True)
    params = module.params
    name = params['name']
    path = params['path']
    link = params['link']
    priority = params['priority']
    UPDATE_ALTERNATIVES = module.get_bin_path('update-alternatives', True)
    current_path = None
    all_alternatives = []
    (rc, display_output, _) = module.run_command(['env', 'LC_ALL=C', UPDATE_ALTERNATIVES, '--display', name])
    if (rc == 0):
        current_path_regex = re.compile('^\\s*link currently points to (.*)$', re.MULTILINE)
        alternative_regex = re.compile('^(\\/.*)\\s-\\spriority', re.MULTILINE)
        match = current_path_regex.search(display_output)
        if match:
            current_path = match.group(1)
        all_alternatives = alternative_regex.findall(display_output)
        if (not link):
            (rc, query_output, _) = module.run_command(['env', 'LC_ALL=C', UPDATE_ALTERNATIVES, '--query', name])
            if (rc == 0):
                for line in query_output.splitlines():
                    if line.startswith('Link:'):
                        link = line.split()[1]
                        break
    if (current_path != path):
        if module.check_mode:
            module.exit_json(changed=True, current_path=current_path)
        try:
            if (path not in all_alternatives):
                if (not os.path.exists(path)):
                    module.fail_json(msg=('Specified path %s does not exist' % path))
                if (not link):
                    module.fail_json(msg='Needed to install the alternative, but unable to do so as we are missing the link')
                module.run_command([UPDATE_ALTERNATIVES, '--install', link, name, path, str(priority)], check_rc=True)
            module.run_command([UPDATE_ALTERNATIVES, '--set', name, path], check_rc=True)
            module.exit_json(changed=True)
        except subprocess.CalledProcessError as cpe:
            module.fail_json(msg=str(dir(cpe)))
    else:
        module.exit_json(changed=False)