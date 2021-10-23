def _disable_zones(self, zones):
    try:
        self.elb.disable_zones(zones)
    except boto.exception.BotoServerError as e:
        self.module.fail_json(msg=('unable to disable zones: %s' % e.message), exception=traceback.format_exc())
    self.changed = True