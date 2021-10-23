def _disable_zones(self, zones):
    try:
        self.elb.disable_zones(zones)
    except boto.exception.BotoServerError as e:
        if ('Invalid Availability Zone' in e.error_message):
            self.module.fail_json(msg=e.error_message)
        else:
            self.module.fail_json(msg='an unknown server error occurred, please try again later')
    self.changed = True