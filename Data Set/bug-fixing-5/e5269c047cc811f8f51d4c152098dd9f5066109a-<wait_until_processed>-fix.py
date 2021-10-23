def wait_until_processed(self, client, wait_timeout, distribution_id, caller_reference):
    if (distribution_id is None):
        distribution_id = self.validate_distribution_from_caller_reference(caller_reference=caller_reference)['Id']
    try:
        waiter = client.get_waiter('distribution_deployed')
        attempts = (1 + int((wait_timeout / 60)))
        waiter.wait(Id=distribution_id, WaiterConfig={
            'MaxAttempts': attempts,
        })
    except botocore.exceptions.WaiterError as e:
        self.module.fail_json(msg='Timeout waiting for cloudfront action. Waited for {0} seconds before timeout. Error: {1}'.format(to_text(wait_timeout), to_native(e)))
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        self.module.fail_json_aws(e, msg='Error getting distribution {0}'.format(distribution_id))