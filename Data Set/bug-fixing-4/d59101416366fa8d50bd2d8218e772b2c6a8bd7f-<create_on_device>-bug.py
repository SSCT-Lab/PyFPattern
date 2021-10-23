def create_on_device(self):
    params = self.changes.api_params()
    params['name'] = self.want.name
    params['partition'] = self.want.partition
    params['placeAfter'] = 'last'
    if self.want.parent_policy:
        uri = 'https://{0}:{1}/mgmt/tm/security/firewall/policy/{2}/rules/'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.parent_policy))
    else:
        uri = 'https://{0}:{1}/mgmt/tm/security/firewall/rule-list/{2}/rules/'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.parent_rule_list))
    if (self.changes.protocol not in ['icmp', 'icmpv6']):
        if (self.changes.icmp_message is not None):
            raise F5ModuleError("The 'icmp_message' can only be specified when 'protocol' is 'icmp' or 'icmpv6'.")
    resp = self.client.api.post(uri, json=params)
    try:
        response = resp.json()
    except ValueError as ex:
        raise F5ModuleError(str(ex))
    if (('code' in response) and (response['code'] in [400, 403])):
        if ('message' in response):
            raise F5ModuleError(response['message'])
        else:
            raise F5ModuleError(resp.content)