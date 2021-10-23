def delete_nvme(self):
    '\n        Delete NVMe service\n        '
    nvme_delete = netapp_utils.zapi.NaElement('nvme-delete')
    try:
        self.server.invoke_successfully(nvme_delete, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error deleting nvme for vserver %s: %s' % (self.parameters['vserver'], to_native(error))))