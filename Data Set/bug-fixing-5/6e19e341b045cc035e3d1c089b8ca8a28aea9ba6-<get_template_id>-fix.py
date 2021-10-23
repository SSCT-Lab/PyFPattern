def get_template_id(module, client, requested_id, requested_name):
    template = (get_template_by_id(module, client, requested_id) if (requested_id is not None) else get_template_by_name(module, client, requested_name))
    if template:
        return template.ID
    else:
        return None