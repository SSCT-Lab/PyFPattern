def _list_topic_subscriptions(self):
    try:
        return self._list_topic_subscriptions_with_backoff()
    except is_boto3_error_code('AuthorizationError'):
        try:
            return [sub for sub in self._list_subscriptions_with_backoff() if (sub['TopicArn'] == self.topic_arn)]
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            self.module.fail_json_aws(e, msg=("Couldn't get subscriptions list for topic %s" % self.topic_arn))
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        self.module.fail_json_aws(e, msg=("Couldn't get subscriptions list for topic %s" % self.topic_arn))