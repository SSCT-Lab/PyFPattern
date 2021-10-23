def _get_elb_info(self, elb):
    elb_info = {
        'name': elb.name,
        'zones': elb.availability_zones,
        'dns_name': elb.dns_name,
        'canonical_hosted_zone_name': elb.canonical_hosted_zone_name,
        'canonical_hosted_zone_name_id': elb.canonical_hosted_zone_name_id,
        'hosted_zone_name': elb.canonical_hosted_zone_name,
        'hosted_zone_id': elb.canonical_hosted_zone_name_id,
        'instances': [instance.id for instance in elb.instances],
        'listeners': self._get_elb_listeners(elb.listeners),
        'scheme': elb.scheme,
        'security_groups': elb.security_groups,
        'health_check': self._get_health_check(elb.health_check),
        'subnets': elb.subnets,
        'instances_inservice': [],
        'instances_inservice_count': 0,
        'instances_outofservice': [],
        'instances_outofservice_count': 0,
        'instances_inservice_percent': 0.0,
        'tags': self._get_tags(elb.name),
    }
    if elb.vpc_id:
        elb_info['vpc_id'] = elb.vpc_id
    if elb.instances:
        try:
            instance_health = self.connection.describe_instance_health(elb.name)
        except BotoServerError as err:
            self.module.fail_json(msg=err.message)
        elb_info['instances_inservice'] = [inst.instance_id for inst in instance_health if (inst.state == 'InService')]
        elb_info['instances_inservice_count'] = len(elb_info['instances_inservice'])
        elb_info['instances_outofservice'] = [inst.instance_id for inst in instance_health if (inst.state == 'OutOfService')]
        elb_info['instances_outofservice_count'] = len(elb_info['instances_outofservice'])
        elb_info['instances_inservice_percent'] = ((float(elb_info['instances_inservice_count']) / (float(elb_info['instances_inservice_count']) + float(elb_info['instances_outofservice_count']))) * 100)
    return elb_info