def disassociate_ip_address(self):
    ip_address = self.get_ip_address()
    if (not ip_address):
        return None
    if ip_address['isstaticnat']:
        self.module.fail_json(msg='IP address is allocated via static nat')
    self.result['changed'] = True
    if (not self.module.check_mode):
        self.module.params['tags'] = []
        ip_address = self.ensure_tags(resource=ip_address, resource_type='publicipaddress')
        res = self.query_api('disassociateIpAddress', id=ip_address['id'])
        poll_async = self.module.params.get('poll_async')
        if poll_async:
            self.poll_job(res, 'ipaddress')
    return ip_address