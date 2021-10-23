

def list_all(self):
    self.log('List app service plans in current subscription')
    try:
        response = list(self.web_client.app_service_plans.list())
    except CloudError as exc:
        self.fail('Error listing app service plans: {1}'.format(str(exc)))
    results = []
    for item in response:
        if self.has_tags(item.tags, self.tags):
            curated_output = self.construct_curated_plan(item)
            results.append(curated_output)
    return results
