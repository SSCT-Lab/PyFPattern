def create_lun(self):
    '\n        Create LUN with requested name and size\n        '
    path = ('/vol/%s/%s' % (self.flexvol_name, self.name))
    lun_create = netapp_utils.zapi.NaElement.create_node_with_children('lun-create-by-size', **{
        'path': path,
        'size': str(self.size),
        'ostype': self.ostype,
        'space-reservation-enabled': str(self.space_reserve),
    })
    try:
        self.server.invoke_successfully(lun_create, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as e:
        self.module.fail_json(msg=('Error provisioning lun %s of size %s: %s' % (self.name, self.size, to_native(e))), exception=traceback.format_exc())