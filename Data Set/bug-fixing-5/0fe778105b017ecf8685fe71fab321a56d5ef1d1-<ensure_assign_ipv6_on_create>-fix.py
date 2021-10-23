def ensure_assign_ipv6_on_create(conn, module, subnet, assign_instances_ipv6, check_mode, start_time):
    if check_mode:
        return
    try:
        conn.modify_subnet_attribute(SubnetId=subnet['id'], AssignIpv6AddressOnCreation={
            'Value': assign_instances_ipv6,
        })
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, msg="Couldn't modify subnet attribute")