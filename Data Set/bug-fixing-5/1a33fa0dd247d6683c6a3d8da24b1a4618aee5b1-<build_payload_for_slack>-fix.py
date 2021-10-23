def build_payload_for_slack(module, text, channel, username, icon_url, icon_emoji, link_names, parse, color, attachments):
    payload = {
        
    }
    if ((color == 'normal') and (text is not None)):
        payload = dict(text=escape_quotes(text))
    elif (text is not None):
        payload = dict(attachments=[dict(text=escape_quotes(text), color=color, mrkdwn_in=['text'])])
    if (channel is not None):
        if ((channel[0] == '#') or (channel[0] == '@')):
            payload['channel'] = channel
        else:
            payload['channel'] = ('#' + channel)
    if (username is not None):
        payload['username'] = username
    if (icon_emoji is not None):
        payload['icon_emoji'] = icon_emoji
    else:
        payload['icon_url'] = icon_url
    if (link_names is not None):
        payload['link_names'] = link_names
    if (parse is not None):
        payload['parse'] = parse
    if (attachments is not None):
        if ('attachments' not in payload):
            payload['attachments'] = []
    if (attachments is not None):
        keys_to_escape = ['title', 'text', 'author_name', 'pretext', 'fallback']
        for attachment in attachments:
            for key in keys_to_escape:
                if (key in attachment):
                    attachment[key] = escape_quotes(attachment[key])
            if ('fallback' not in attachment):
                attachment['fallback'] = attachment['text']
            payload['attachments'].append(attachment)
    payload = module.jsonify(payload)
    return payload