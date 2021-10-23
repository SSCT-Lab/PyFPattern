def _get_vpc_connection(module, region, aws_connect_params):
    try:
        return connect_to_aws(boto.vpc, region, **aws_connect_params)
    except (boto.exception.NoAuthHandlerFound, AnsibleAWSError) as e:
        module.fail_json(msg=str(e))