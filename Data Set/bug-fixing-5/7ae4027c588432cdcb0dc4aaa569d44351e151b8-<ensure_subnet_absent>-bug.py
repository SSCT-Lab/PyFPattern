def ensure_subnet_absent(conn, module, vpc_id, cidr, check_mode):
    subnet = get_matching_subnet(conn, vpc_id, cidr)
    if (subnet is None):
        return {
            'changed': False,
        }
    try:
        conn.delete_subnet(SubnetId=subnet['id'], DryRun=check_mode)
        return {
            'changed': True,
        }
    except ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))