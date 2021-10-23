def modify_nvme(self, status=None):
    '\n        Modify NVMe service\n        '
    if (status is None):
        status = self.parameters['status_admin']
    options = {
        'is-available': status,
    }
    nvme_modify = netapp_utils.zapi.NaElement('nvme-modify')
    nvme_modify.translate_struct(options)
    try:
        self.server.invoke_successfully(nvme_modify, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error modifying nvme for vserver %s: %s' % (self.parameters['vserver'], to_native(error))), exception=traceback.format_exc())