

def main():
    module = AnsibleModule(argument_spec=dict(user=dict(required=True), password=dict(required=True, no_log=True), to=dict(required=True), msg=dict(required=True), host=dict(required=False), port=dict(required=False, default=5222), encoding=dict(required=False)), supports_check_mode=True)
    if (not HAS_XMPP):
        module.fail_json(msg='The required python xmpp library (xmpppy) is not installed')
    jid = xmpp.JID(module.params['user'])
    user = jid.getNode()
    server = jid.getDomain()
    port = module.params['port']
    password = module.params['password']
    try:
        (to, nick) = module.params['to'].split('/', 1)
    except ValueError:
        (to, nick) = (module.params['to'], None)
    if module.params['host']:
        host = module.params['host']
    else:
        host = server
    if module.params['encoding']:
        xmpp.simplexml.ENCODING = module.params['encoding']
    msg = xmpp.protocol.Message(body=module.params['msg'])
    try:
        conn = xmpp.Client(server, debug=[])
        if (not conn.connect(server=(host, port))):
            module.fail_json(rc=1, msg=('Failed to connect to server: %s' % server))
        if (not conn.auth(user, password, 'Ansible')):
            module.fail_json(rc=1, msg=('Failed to authorize %s on: %s' % (user, server)))
        conn.sendInitPresence(requestRoster=0)
        if nick:
            msg.setType('groupchat')
            msg.setTag('x', namespace='http://jabber.org/protocol/muc#user')
            join = xmpp.Presence(to=module.params['to'])
            join.setTag('x', namespace='http://jabber.org/protocol/muc')
            conn.send(join)
            time.sleep(1)
        else:
            msg.setType('chat')
        msg.setTo(to)
        if (not module.check_mode):
            conn.send(msg)
        time.sleep(1)
        conn.disconnect()
    except Exception as e:
        module.fail_json(msg=('unable to send msg: %s' % to_native(e)), exception=traceback.format_exc())
    module.exit_json(changed=False, to=to, user=user, msg=msg.getBody())
