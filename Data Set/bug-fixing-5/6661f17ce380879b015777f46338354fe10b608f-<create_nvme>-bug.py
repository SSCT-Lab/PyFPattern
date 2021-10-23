def create_nvme(self):
    '\n        Create NVMe service\n        '
    nvme_create = netapp_utils.zapi.NaElement('nvme-create')
    if (self.parameters.get('status_admin') is not None):
        options = {
            'is-available': self.parameters['status_admin'],
        }
        nvme_create.translate_struct(options)
    try:
        self.server.invoke_successfully(nvme_create, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error creating nvme for vserver %s: %s' % (self.parameters['vserver'], to_native(error))))