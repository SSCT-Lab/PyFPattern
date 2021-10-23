

def find_asgs(conn, module, name=None, tags=None):
    '\n    Args:\n        conn (boto3.AutoScaling.Client): Valid Boto3 ASG client.\n        name (str): Optional name of the ASG you are looking for.\n        tags (dict): Optional dictionary of tags and values to search for.\n\n    Basic Usage:\n        >>> name = \'public-webapp-production\'\n        >>> tags = { \'env\': \'production\' }\n        >>> conn = boto3.client(\'autoscaling\', region_name=\'us-west-2\')\n        >>> results = find_asgs(name, conn)\n\n    Returns:\n        List\n        [\n            {\n                "auto_scaling_group_arn": "arn:aws:autoscaling:us-west-2:275977225706:autoScalingGroup:58abc686-9783-4528-b338-3ad6f1cbbbaf:autoScalingGroupName/public-webapp-production",\n                "auto_scaling_group_name": "public-webapp-production",\n                "availability_zones": ["us-west-2c", "us-west-2b", "us-west-2a"],\n                "created_time": "2016-02-02T23:28:42.481000+00:00",\n                "default_cooldown": 300,\n                "desired_capacity": 2,\n                "enabled_metrics": [],\n                "health_check_grace_period": 300,\n                "health_check_type": "ELB",\n                "instances":\n                [\n                    {\n                        "availability_zone": "us-west-2c",\n                        "health_status": "Healthy",\n                        "instance_id": "i-047a12cb",\n                        "launch_configuration_name": "public-webapp-production-1",\n                        "lifecycle_state": "InService",\n                        "protected_from_scale_in": false\n                    },\n                    {\n                        "availability_zone": "us-west-2a",\n                        "health_status": "Healthy",\n                        "instance_id": "i-7a29df2c",\n                        "launch_configuration_name": "public-webapp-production-1",\n                        "lifecycle_state": "InService",\n                        "protected_from_scale_in": false\n                    }\n                ],\n                "launch_configuration_name": "public-webapp-production-1",\n                "load_balancer_names": ["public-webapp-production-lb"],\n                "max_size": 4,\n                "min_size": 2,\n                "new_instances_protected_from_scale_in": false,\n                "placement_group": None,\n                "status": None,\n                "suspended_processes": [],\n                "tags":\n                [\n                    {\n                        "key": "Name",\n                        "propagate_at_launch": true,\n                        "resource_id": "public-webapp-production",\n                        "resource_type": "auto-scaling-group",\n                        "value": "public-webapp-production"\n                    },\n                    {\n                        "key": "env",\n                        "propagate_at_launch": true,\n                        "resource_id": "public-webapp-production",\n                        "resource_type": "auto-scaling-group",\n                        "value": "production"\n                    }\n                ],\n                "termination_policies":\n                [\n                    "Default"\n                ],\n                "vpc_zone_identifier":\n                [\n                    "subnet-a1b1c1d1",\n                    "subnet-a2b2c2d2",\n                    "subnet-a3b3c3d3"\n                ]\n            }\n        ]\n    '
    try:
        asgs_paginator = conn.get_paginator('describe_auto_scaling_groups')
        asgs = asgs_paginator.paginate().build_full_result()
    except ClientError as e:
        module.fail_json(msg=e.message, **camel_dict_to_snake_dict(e.response))
    matched_asgs = []
    if (name is not None):
        name_prog = re.compile(('^' + name))
    for asg in asgs['AutoScalingGroups']:
        if name:
            matched_name = name_prog.search(asg['AutoScalingGroupName'])
        else:
            matched_name = True
        if tags:
            matched_tags = match_asg_tags(tags, asg)
        else:
            matched_tags = True
        if (matched_name and matched_tags):
            matched_asgs.append(camel_dict_to_snake_dict(asg))
    return matched_asgs
