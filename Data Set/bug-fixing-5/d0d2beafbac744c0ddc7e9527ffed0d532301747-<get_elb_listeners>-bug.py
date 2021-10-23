def get_elb_listeners(connection, module, elb_arn):
    try:
        return connection.describe_listeners(LoadBalancerArn=elb_arn)['Listeners']
    except ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))