def get_configuration(self):
    configuration = None
    args = self._get_common_configuration_args()
    configurations = self.query_api('listConfigurations', **args)
    if (not configurations):
        self.module.fail_json(msg=('Configuration %s not found.' % args['name']))
    configuration = configurations['configuration'][0]
    return configuration