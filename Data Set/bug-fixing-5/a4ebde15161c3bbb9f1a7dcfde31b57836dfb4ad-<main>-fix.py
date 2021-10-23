def main():
    module = AnsibleModule(argument_spec=dict(token=dict(required=True, no_log=True), msg=dict(required=True), type=dict(required=True, choices=['inbox', 'chat']), external_user_name=dict(required=False), from_address=dict(required=False), source=dict(required=False), subject=dict(required=False), from_name=dict(required=False), reply_to=dict(required=False), project=dict(required=False), tags=dict(required=False), link=dict(required=False), validate_certs=dict(default='yes', type='bool')), supports_check_mode=True)
    type = module.params['type']
    token = module.params['token']
    if (type == 'inbox'):
        url = ('https://api.flowdock.com/v1/messages/team_inbox/%s' % token)
    else:
        url = ('https://api.flowdock.com/v1/messages/chat/%s' % token)
    params = {
        
    }
    params['content'] = module.params['msg']
    if module.params['external_user_name']:
        if (type == 'inbox'):
            module.fail_json(msg="external_user_name is not valid for the 'inbox' type")
        else:
            params['external_user_name'] = module.params['external_user_name']
    elif (type == 'chat'):
        module.fail_json(msg="external_user_name is required for the 'chat' type")
    for item in ['from_address', 'source', 'subject']:
        if module.params[item]:
            if (type == 'chat'):
                module.fail_json(msg=("%s is not valid for the 'chat' type" % item))
            else:
                params[item] = module.params[item]
        elif (type == 'inbox'):
            module.fail_json(msg=("%s is required for the 'inbox' type" % item))
    if module.params['tags']:
        params['tags'] = module.params['tags']
    for item in ['from_name', 'reply_to', 'project', 'link']:
        if module.params[item]:
            if (type == 'chat'):
                module.fail_json(msg=("%s is not valid for the 'chat' type" % item))
            else:
                params[item] = module.params[item]
    if module.check_mode:
        module.exit_json(changed=False)
    data = urlencode(params)
    (response, info) = fetch_url(module, url, data=data)
    if (info['status'] != 200):
        module.fail_json(msg=('unable to send msg: %s' % info['msg']))
    module.exit_json(changed=True, msg=module.params['msg'])