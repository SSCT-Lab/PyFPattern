def edit_provider(self, provider, name, provider_type, endpoints, zone_id, provider_region, host_default_vnc_port_start, host_default_vnc_port_end, subscription, project, uid_ems, tenant_mapping_enabled, api_version):
    ' Edit a provider from manageiq.\n\n        Returns:\n            a short message describing the operation executed.\n        '
    url = ('%s/providers/%s' % (self.api_url, provider['id']))
    resource = dict(name=name, zone={
        'id': zone_id,
    }, provider_region=provider_region, connection_configurations=endpoints, host_default_vnc_port_start=host_default_vnc_port_start, host_default_vnc_port_end=host_default_vnc_port_end, subscription=subscription, project=project, uid_ems=uid_ems, tenant_mapping_enabled=tenant_mapping_enabled, api_version=api_version)
    resource = delete_nulls(resource)
    try:
        result = self.client.post(url, action='edit', resource=resource)
    except Exception as e:
        self.module.fail_json(msg=('failed to update provider %s: %s' % (provider['name'], str(e))))
    return dict(changed=True, msg=('successfully updated the provider %s: %s' % (provider['name'], result)))