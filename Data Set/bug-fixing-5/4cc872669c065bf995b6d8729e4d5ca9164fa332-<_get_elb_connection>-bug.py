def _get_elb_connection(self):
    try:
        return connect_to_aws(boto.ec2.elb, self.region, **self.aws_connect_params)
    except (boto.exception.NoAuthHandlerFound, AnsibleAWSError) as e:
        self.module.fail_json(msg=str(e))