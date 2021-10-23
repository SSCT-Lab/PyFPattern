def build_attachment_text(group, event=None):
    ev_metadata = group.get_event_metadata()
    ev_type = group.get_event_type()
    if (ev_type == 'error'):
        return (ev_metadata.get('value') or ev_metadata.get('function'))
    else:
        return None