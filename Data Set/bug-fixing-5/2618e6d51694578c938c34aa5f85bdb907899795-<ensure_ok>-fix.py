@_throttleable_operation(_THROTTLING_RETRIES)
def ensure_ok(self):
    'Create the ELB'
    if (not self.elb):
        self._create_elb()
    elif self._get_scheme():
        self.ensure_gone()
        self._create_elb()
    else:
        self._set_zones()
        self._set_security_groups()
        self._set_elb_listeners()
        self._set_subnets()
    self._set_health_check()
    if self._check_attribute_support('connection_draining'):
        self._set_connection_draining_timeout()
    if self._check_attribute_support('connecting_settings'):
        self._set_idle_timeout()
    if self._check_attribute_support('cross_zone_load_balancing'):
        self._set_cross_az_load_balancing()
    if self._check_attribute_support('access_log'):
        self._set_access_log()
    self.select_stickiness_policy()
    self._set_backend_policies()
    self._set_instance_ids()
    self._set_tags()