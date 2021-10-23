def _enable_zones(self, zones):
    try:
        self.elb.enable_zones(zones)
    except boto.exception.BotoServerError as e:
        self.module.fail_json(msg=('unable to enable zones: %s' % e.message), exception=traceback.format_exc())
    self.changed = True