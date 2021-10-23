

def get_target_group_attributes(connection, module, target_group_arn):
    try:
        target_group_attributes = boto3_tag_list_to_ansible_dict(connection.describe_target_group_attributes(TargetGroupArn=target_group_arn)['Attributes'])
    except ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    for (k, v) in target_group_attributes.items():
        target_group_attributes[k.replace('.', '_')] = v
        del target_group_attributes[k]
    return target_group_attributes
