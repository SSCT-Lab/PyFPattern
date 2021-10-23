def exists(self):
    name = self.want.name
    if self.want.parent_policy:
        uri = 'https://{0}:{1}/mgmt/tm/security/firewall/policy/{2}/rules/{3}'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.parent_policy), name.replace('/', '_'))
    else:
        uri = 'https://{0}:{1}/mgmt/tm/security/firewall/rule-list/{2}/rules/{3}'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.parent_rule_list), name.replace('/', '_'))
    resp = self.client.api.get(uri)
    if resp.ok:
        return True
    return False