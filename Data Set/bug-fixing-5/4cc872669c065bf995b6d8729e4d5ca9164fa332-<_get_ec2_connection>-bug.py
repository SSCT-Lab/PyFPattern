def _get_ec2_connection(self):
    try:
        return connect_to_aws(boto.ec2, self.region, **self.aws_connect_params)
    except (boto.exception.NoAuthHandlerFound, StandardError) as e:
        self.module.fail_json(msg=str(e))