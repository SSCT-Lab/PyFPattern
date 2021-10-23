def get_properties(autoscaling_group):
    properties = dict(((attr, getattr(autoscaling_group, attr)) for attr in ASG_ATTRIBUTES))
    if (('tags' in properties) and isinstance(properties['tags'], list)):
        serializable_tags = {
            
        }
        for tag in properties['tags']:
            serializable_tags[tag.key] = [tag.value, tag.propagate_at_launch]
        properties['tags'] = serializable_tags
    properties['healthy_instances'] = 0
    properties['in_service_instances'] = 0
    properties['unhealthy_instances'] = 0
    properties['pending_instances'] = 0
    properties['viable_instances'] = 0
    properties['terminating_instances'] = 0
    instance_facts = {
        
    }
    if autoscaling_group.instances:
        properties['instances'] = [i.instance_id for i in autoscaling_group.instances]
        for i in autoscaling_group.instances:
            instance_facts[i.instance_id] = {
                'health_status': i.health_status,
                'lifecycle_state': i.lifecycle_state,
                'launch_config_name': i.launch_config_name,
            }
            if ((i.health_status == 'Healthy') and (i.lifecycle_state == 'InService')):
                properties['viable_instances'] += 1
            if (i.health_status == 'Healthy'):
                properties['healthy_instances'] += 1
            else:
                properties['unhealthy_instances'] += 1
            if (i.lifecycle_state == 'InService'):
                properties['in_service_instances'] += 1
            if (i.lifecycle_state == 'Terminating'):
                properties['terminating_instances'] += 1
            if (i.lifecycle_state == 'Pending'):
                properties['pending_instances'] += 1
    else:
        properties['instances'] = []
    properties['instance_facts'] = instance_facts
    properties['load_balancers'] = autoscaling_group.load_balancers
    if getattr(autoscaling_group, 'tags', None):
        properties['tags'] = dict(((t.key, t.value) for t in autoscaling_group.tags))
    return properties