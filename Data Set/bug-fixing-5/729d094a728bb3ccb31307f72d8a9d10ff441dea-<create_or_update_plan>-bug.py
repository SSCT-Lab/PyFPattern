def create_or_update_plan(self):
    '\n        Creates app service plan\n        :return: deserialized app service plan dictionary\n        '
    self.log('Create App Service Plan {0}'.format(self.name))
    try:
        sku = _normalize_sku(self.sku)
        sku_def = SkuDescription(tier=get_sku_name(sku), name=sku, capacity=self.number_of_workers)
        plan_def = AppServicePlan(location=self.location, app_service_plan_name=self.name, sku=sku_def, reserved=self.is_linux, tags=(self.tags if self.tags else None))
        poller = self.web_client.app_service_plans.create_or_update(self.resource_group, self.name, plan_def)
        if isinstance(poller, AzureOperationPoller):
            response = self.get_poller_result(poller)
        self.log('Response : {0}'.format(response))
        return response.as_dict()
    except CloudError as ex:
        self.fail('Failed to create app service plan {0} in resource group {1}: {2}'.format(self.name, self.resource_group, str(ex)))