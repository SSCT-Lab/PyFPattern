

def build_attachment_text(group, event=None):
    obj = (event if (event is not None) else group)
    ev_metadata = obj.get_event_metadata()
    ev_type = obj.get_event_type()
    if (ev_type == 'error'):
        return (ev_metadata.get('value') or ev_metadata.get('function'))
    else:
        return None
