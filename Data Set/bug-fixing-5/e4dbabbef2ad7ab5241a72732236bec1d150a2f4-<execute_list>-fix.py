def execute_list(self):
    '\n        lists the roles installed on the local system or matches a single role passed as an argument.\n        '
    if (len(self.args) > 1):
        raise AnsibleOptionsError('- please specify only one role to list, or specify no roles to see a full list')
    if (len(self.args) == 1):
        name = self.args.pop()
        gr = GalaxyRole(self.galaxy, name)
        if gr.metadata:
            install_info = gr.install_info
            version = None
            if install_info:
                version = install_info.get('version', None)
            if (not version):
                version = '(unknown version)'
            display.display(('- %s, %s' % (name, version)))
        else:
            display.display(('- the role %s was not found' % name))
    else:
        roles_path = self.options.roles_path
        path_found = False
        for path in roles_path:
            role_path = os.path.expanduser(path)
            if (not os.path.exists(role_path)):
                display.warning(('- the configured path %s does not exist.' % role_path))
                continue
            elif (not os.path.isdir(role_path)):
                display.warning(('- the configured path %s, exists, but it is not a directory.' % role_path))
                continue
            path_files = os.listdir(role_path)
            path_found = True
            for path_file in path_files:
                gr = GalaxyRole(self.galaxy, path_file)
                if gr.metadata:
                    install_info = gr.install_info
                    version = None
                    if install_info:
                        version = install_info.get('version', None)
                    if (not version):
                        version = '(unknown version)'
                    display.display(('- %s, %s' % (path_file, version)))
        if (not path_found):
            raise AnsibleOptionsError('- None of the provided paths was usable. Please specify a valid path with --roles-path')
    return 0