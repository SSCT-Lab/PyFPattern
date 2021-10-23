def get_elb_attributes(connection, module, elb_arn):
    try:
        elb_attributes = boto3_tag_list_to_ansible_dict(connection.describe_load_balancer_attributes(LoadBalancerArn=elb_arn)['Attributes'])
    except ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    for (k, v) in elb_attributes.items():
        elb_attributes[k.replace('.', '_')] = v
        del elb_attributes[k]
    return elb_attributes