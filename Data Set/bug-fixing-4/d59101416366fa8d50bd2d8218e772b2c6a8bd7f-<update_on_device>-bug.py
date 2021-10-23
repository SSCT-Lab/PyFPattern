def update_on_device(self):
    if self.want.parent_policy:
        uri = 'https://{0}:{1}/mgmt/tm/security/firewall/policy/{2}/rules/{3}'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.parent_policy), self.want.name)
    else:
        uri = 'https://{0}:{1}/mgmt/tm/security/firewall/rule-list/{2}/rules/{3}'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.parent_rule_list), self.want.name)
    if ((self.have.protocol not in ['icmp', 'icmpv6']) and (self.changes.protocol not in ['icmp', 'icmpv6'])):
        if (self.changes.icmp_message is not None):
            raise F5ModuleError("The 'icmp_message' can only be specified when 'protocol' is 'icmp' or 'icmpv6'.")
    if (self.changes.protocol in ['icmp', 'icmpv6']):
        self.changes.update({
            'source': {
                
            },
        })
        self.changes.update({
            'destination': {
                
            },
        })
    params = self.changes.api_params()
    resp = self.client.api.patch(uri, json=params)
    try:
        response = resp.json()
    except ValueError as ex:
        raise F5ModuleError(str(ex))
    if (('code' in response) and (response['code'] == 400)):
        if ('message' in response):
            raise F5ModuleError(response['message'])
        else:
            raise F5ModuleError(resp.content)