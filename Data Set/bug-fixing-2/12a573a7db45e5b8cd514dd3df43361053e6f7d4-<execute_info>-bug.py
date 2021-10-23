

def execute_info(self):
    '\n        prints out detailed information about an installed role as well as info available from the galaxy API.\n        '
    if (len(self.args) == 0):
        raise AnsibleOptionsError('- you must specify a user/role name')
    roles_path = self.options.roles_path
    data = ''
    for role in self.args:
        role_info = {
            'path': roles_path,
        }
        gr = GalaxyRole(self.galaxy, role)
        install_info = gr.install_info
        if install_info:
            if ('version' in install_info):
                install_info['intalled_version'] = install_info['version']
                del install_info['version']
            role_info.update(install_info)
        remote_data = False
        if (not self.options.offline):
            remote_data = self.api.lookup_role_by_name(role, False)
        if remote_data:
            role_info.update(remote_data)
        if gr.metadata:
            role_info.update(gr.metadata)
        req = RoleRequirement()
        role_spec = req.role_yaml_parse({
            'role': role,
        })
        if role_spec:
            role_info.update(role_spec)
        data = self._display_role_info(role_info)
        if (not data):
            data = ('\n- the role %s was not found' % role)
    self.pager(data)
