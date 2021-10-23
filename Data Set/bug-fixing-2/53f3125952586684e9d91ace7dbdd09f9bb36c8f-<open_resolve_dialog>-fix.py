

def open_resolve_dialog(self, data, group, integration):
    callback_id = json.dumps({
        'issue': group.id,
        'orig_response_url': data['response_url'],
        'is_message': self.is_message(data),
    })
    dialog = {
        'callback_id': callback_id,
        'title': 'Resolve Issue',
        'submit_label': 'Resolve',
        'elements': [RESOLVE_SELECTOR],
    }
    payload = {
        'dialog': json.dumps(dialog),
        'trigger_id': data['trigger_id'],
        'token': integration.metadata['access_token'],
    }
    session = http.build_session()
    req = session.post('https://slack.com/api/dialog.open', data=payload)
    resp = req.json()
    if (not resp.get('ok')):
        logger.error('slack.action.response-error', extra={
            'response': resp,
        })
