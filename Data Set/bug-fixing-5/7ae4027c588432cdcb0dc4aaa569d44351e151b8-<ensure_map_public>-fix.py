def ensure_map_public(conn, module, subnet, map_public, check_mode):
    if check_mode:
        return
    try:
        conn.modify_subnet_attribute(SubnetId=subnet['id'], MapPublicIpOnLaunch={
            'Value': map_public,
        })
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))