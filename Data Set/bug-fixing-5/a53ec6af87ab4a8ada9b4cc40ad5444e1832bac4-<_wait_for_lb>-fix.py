def _wait_for_lb(module, cloud, lb, status, failures, interval=5):
    'Wait for load balancer to be in a particular provisioning status.'
    timeout = module.params['timeout']
    total_sleep = 0
    if (failures is None):
        failures = []
    while (total_sleep < timeout):
        lb = cloud.load_balancer.find_load_balancer(lb.id)
        if lb:
            if (lb.provisioning_status == status):
                return None
            if (lb.provisioning_status in failures):
                module.fail_json(msg=('Load Balancer %s transitioned to failure state %s' % (lb.id, lb.provisioning_status)))
        elif (status == 'DELETED'):
            return None
        else:
            module.fail_json(msg=('Load Balancer %s transitioned to DELETED' % lb.id))
        time.sleep(interval)
        total_sleep += interval
    module.fail_json(msg=('Timeout waiting for Load Balancer %s to transition to %s' % (lb.id, status)))