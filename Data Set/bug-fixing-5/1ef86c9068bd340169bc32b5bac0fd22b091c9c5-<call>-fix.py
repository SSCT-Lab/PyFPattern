def call(self, method: str, api_params: dict) -> None:
    '\n        Calls the Slack client.\n\n        :param method: method\n        :param api_params: parameters of the API\n        '
    slack_client = SlackClient(self.token)
    return_code = slack_client.api_call(method, **api_params)
    if (not return_code['ok']):
        msg = 'Slack API call failed ({})'.format(return_code['error'])
        raise AirflowException(msg)