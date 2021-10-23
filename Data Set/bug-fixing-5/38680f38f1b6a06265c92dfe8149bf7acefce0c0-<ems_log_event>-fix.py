def ems_log_event(self, state):
    'Autosupport log event'
    if (state == 'create'):
        message = (('A Volume has been created, size: ' + str(self.parameters['size'])) + str(self.parameters['size_unit']))
    elif (state == 'delete'):
        message = 'A Volume has been deleted'
    elif (state == 'move'):
        message = 'A Volume has been moved'
    elif (state == 'rename'):
        message = 'A Volume has been renamed'
    elif (state == 'resize'):
        message = (('A Volume has been resized to: ' + str(self.parameters['size'])) + str(self.parameters['size_unit']))
    elif (state == 'change'):
        message = 'A Volume state has been changed'
    else:
        message = 'na_ontap_volume has been called'
    netapp_utils.ems_log_event('na_ontap_volume', self.server, event=message)