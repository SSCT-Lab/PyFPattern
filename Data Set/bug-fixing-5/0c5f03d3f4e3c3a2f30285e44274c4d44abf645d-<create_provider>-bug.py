def create_provider(self, name, provider_type, endpoints, zone_id, provider_region, host_default_vnc_port_start, host_default_vnc_port_end, subscription, project, uid_ems, tenant_mapping_enabled, api_version):
    ' Creates the user in manageiq.\n\n        Returns:\n            the created user id, name, created_on timestamp,\n            updated_on timestamp, userid and current_group_id.\n        '
    endpoints = delete_nulls(endpoints)
    try:
        url = ('%s/providers' % self.api_url)
        result = self.client.post(url, name=name, type=supported_providers()[provider_type]['class_name'], zone={
            'id': zone_id,
        }, provider_region=provider_region, host_default_vnc_port_start=host_default_vnc_port_start, host_default_vnc_port_end=host_default_vnc_port_end, subscription=subscription, project=project, uid_ems=uid_ems, tenant_mapping_enabled=tenant_mapping_enabled, api_version=api_version, connection_configurations=endpoints)
    except Exception as e:
        self.module.fail_json(msg=('failed to create provider %s: %s' % (name, str(e))))
    return dict(changed=True, msg=('successfully created the provider %s: %s' % (name, result['results'])))