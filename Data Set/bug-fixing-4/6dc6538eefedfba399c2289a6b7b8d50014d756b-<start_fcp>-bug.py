def start_fcp(self):
    '\n        Starts an existing FCP\n        :return: none\n        '
    try:
        self.server.invoke_successfully(netapp_utils.zapi.NaElement('fcp-service-start'), True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error starting FCP %s' % to_native(error)), exception=traceback.format_exc())