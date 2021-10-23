

def update_service(self, name, old_service, new_service):
    service_data = new_service.build_docker_service(self.get_networks_names_ids())
    result = self.client.update_service(old_service.service_id, old_service.service_version, name=name, **service_data)
    self.client.report_warnings(result, ['Warning'])
