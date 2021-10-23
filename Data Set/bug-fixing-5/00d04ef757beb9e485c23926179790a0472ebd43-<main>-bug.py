def main():
    module = AnsibleModule(argument_spec=dict(account_sid=dict(required=True), auth_token=dict(required=True, no_log=True), msg=dict(required=True), from_number=dict(required=True), to_number=dict(required=True), media_url=dict(default=None, required=False)), supports_check_mode=True)
    account_sid = module.params['account_sid']
    auth_token = module.params['auth_token']
    msg = module.params['msg']
    from_number = module.params['from_number']
    to_number = module.params['to_number']
    media_url = module.params['media_url']
    if (not isinstance(to_number, list)):
        to_number = [to_number]
    for number in to_number:
        (r, info) = post_twilio_api(module, account_sid, auth_token, msg, from_number, number, media_url)
        if (info['status'] not in [200, 201]):
            body_message = 'unknown error'
            if ('body' in info):
                body = json.loads(info['body'])
                body_message = body['message']
            module.fail_json(msg=('unable to send message to %s: %s' % (number, body_message)))
    module.exit_json(msg=msg, changed=False)