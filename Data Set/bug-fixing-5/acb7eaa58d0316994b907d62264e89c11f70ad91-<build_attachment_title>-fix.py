def build_attachment_title(group, event=None):
    ev_metadata = group.get_event_metadata()
    ev_type = group.get_event_type()
    if (ev_type == 'error'):
        if ('type' in ev_metadata):
            if group.culprit:
                return '{} - {}'.format(ev_metadata['type'][:40], group.culprit)
            return ev_metadata['type']
        if group.culprit:
            return '{} - {}'.format(group.title, group.culprit)
        return group.title
    elif (ev_type == 'csp'):
        return '{} - {}'.format(ev_metadata['directive'], ev_metadata['uri'])
    else:
        if group.culprit:
            return '{} - {}'.format(group.title, group.culprit)
        return group.title