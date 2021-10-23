def _create_cluster(self):
    required_params = ['cluster_type', 'hypervisor']
    self.module.fail_on_missing_params(required_params=required_params)
    args = self._get_common_cluster_args()
    args['zoneid'] = self.get_zone(key='id')
    args['podid'] = self.get_pod(key='id')
    args['url'] = self.module.params.get('url')
    args['username'] = self.module.params.get('username')
    args['password'] = self.module.params.get('password')
    args['guestvswitchname'] = self.module.params.get('guest_vswitch_name')
    args['guestvswitchtype'] = self.module.params.get('guest_vswitch_type')
    args['publicvswitchtype'] = self.module.params.get('public_vswitch_name')
    args['publicvswitchtype'] = self.module.params.get('public_vswitch_type')
    args['vsmipaddress'] = self.module.params.get('vms_ip_address')
    args['vsmusername'] = self.module.params.get('vms_username')
    args['vmspassword'] = self.module.params.get('vms_password')
    args['ovm3cluster'] = self.module.params.get('ovm3_cluster')
    args['ovm3pool'] = self.module.params.get('ovm3_pool')
    args['ovm3vip'] = self.module.params.get('ovm3_vip')
    self.result['changed'] = True
    cluster = None
    if (not self.module.check_mode):
        res = self.query_api('addCluster', **args)
        if ('errortext' in res):
            self.module.fail_json(msg=("Failed: '%s'" % res['errortext']))
        if isinstance(res['cluster'], list):
            cluster = res['cluster'][0]
        else:
            cluster = res['cluster']
    return cluster