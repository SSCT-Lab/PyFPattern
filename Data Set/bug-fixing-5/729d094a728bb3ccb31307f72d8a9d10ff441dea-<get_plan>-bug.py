def get_plan(self):
    '\n        Gets app service plan\n        :return: deserialized app service plan dictionary\n        '
    self.log('Get App Service Plan {0}'.format(self.name))
    try:
        response = self.web_client.app_service_plans.get(self.resource_group, self.name)
        self.log('Response : {0}'.format(response))
        self.log('App Service Plan : {0} found'.format(response.name))
        return response.as_dict()
    except CloudError as ex:
        self.log("Didn't find app service plan {0} in resource group {1}".format(self.name, self.resource_group))
    return False