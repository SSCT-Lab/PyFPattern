@ensure_connected
def get_configuration(self, format='xml', filter=None):
    '\n        Retrieve all or part of a specified configuration.\n        :param format: format in which configuration should be retrieved\n        :param filter: specifies the portion of the configuration to retrieve\n        :return: Received rpc response from remote host in string format\n        '
    return self.m.get_configuration(format=format, filter=filter).data_xml