def create_cifs_server(self):
    '\n        calling zapi to create cifs_server\n        '
    options = {
        'cifs-server': self.cifs_server_name,
        'administrative-status': ('up' if (self.service_state == 'started') else 'down'),
    }
    if (self.workgroup is not None):
        options['workgroup'] = self.workgroup
    if (self.domain is not None):
        options['domain'] = self.domain
    if (self.admin_user_name is not None):
        options['admin-username'] = self.admin_user_name
    if (self.admin_password is not None):
        options['admin-password'] = self.admin_password
    cifs_server_create = netapp_utils.zapi.NaElement.create_node_with_children('cifs-server-create', **options)
    try:
        self.server.invoke_successfully(cifs_server_create, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as exc:
        self.module.fail_json(msg=('Error Creating cifs_server %s: %s' % (self.cifs_server_name, to_native(exc))), exception=traceback.format_exc())