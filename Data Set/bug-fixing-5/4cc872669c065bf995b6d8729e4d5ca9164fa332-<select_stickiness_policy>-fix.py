def select_stickiness_policy(self):
    if self.stickiness:
        if (('cookie' in self.stickiness) and ('expiration' in self.stickiness)):
            self.module.fail_json(msg="'cookie' and 'expiration' can not be set at the same time")
        elb_info = self.elb_conn.get_all_load_balancers(self.elb.name)[0]
        d = {
            
        }
        for listener in elb_info.listeners:
            d[listener[0]] = listener[2]
        listeners_dict = d
        if (self.stickiness['type'] == 'loadbalancer'):
            policy = []
            policy_type = 'LBCookieStickinessPolicyType'
            if self.module.boolean(self.stickiness['enabled']):
                if ('expiration' not in self.stickiness):
                    self.module.fail_json(msg='expiration must be set when type is loadbalancer')
                expiration = (self.stickiness['expiration'] if (self.stickiness['expiration'] is not 0) else None)
                policy_attrs = {
                    'type': policy_type,
                    'attr': 'lb_cookie_stickiness_policies',
                    'method': 'create_lb_cookie_stickiness_policy',
                    'dict_key': 'cookie_expiration_period',
                    'param_value': expiration,
                }
                policy.append(self._policy_name(policy_attrs['type']))
                self._set_stickiness_policy(elb_info, listeners_dict, policy, **policy_attrs)
            elif (not self.module.boolean(self.stickiness['enabled'])):
                if len(elb_info.policies.lb_cookie_stickiness_policies):
                    if (elb_info.policies.lb_cookie_stickiness_policies[0].policy_name == self._policy_name(policy_type)):
                        self.changed = True
                else:
                    self.changed = False
                self._set_listener_policy(listeners_dict)
                self._delete_policy(self.elb.name, self._policy_name(policy_type))
        elif (self.stickiness['type'] == 'application'):
            policy = []
            policy_type = 'AppCookieStickinessPolicyType'
            if self.module.boolean(self.stickiness['enabled']):
                if ('cookie' not in self.stickiness):
                    self.module.fail_json(msg='cookie must be set when type is application')
                policy_attrs = {
                    'type': policy_type,
                    'attr': 'app_cookie_stickiness_policies',
                    'method': 'create_app_cookie_stickiness_policy',
                    'dict_key': 'cookie_name',
                    'param_value': self.stickiness['cookie'],
                }
                policy.append(self._policy_name(policy_attrs['type']))
                self._set_stickiness_policy(elb_info, listeners_dict, policy, **policy_attrs)
            elif (not self.module.boolean(self.stickiness['enabled'])):
                if len(elb_info.policies.app_cookie_stickiness_policies):
                    if (elb_info.policies.app_cookie_stickiness_policies[0].policy_name == self._policy_name(policy_type)):
                        self.changed = True
                self._set_listener_policy(listeners_dict)
                self._delete_policy(self.elb.name, self._policy_name(policy_type))
        else:
            self._set_listener_policy(listeners_dict)