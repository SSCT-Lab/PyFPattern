@_throttleable_operation(_THROTTLING_RETRIES)
def _wait_for_elb_removed(self):
    polling_increment_secs = 15
    max_retries = (self.wait_timeout / polling_increment_secs)
    status_achieved = False
    for x in range(0, max_retries):
        try:
            self.elb_conn.get_all_lb_attributes(self.name)
        except (boto.exception.BotoServerError, StandardError) as e:
            if ('LoadBalancerNotFound' in e.code):
                status_achieved = True
                break
            else:
                time.sleep(polling_increment_secs)
    return status_achieved