

def find_reference_event(reference_event):
    try:
        (project_slug, event_id) = reference_event.slug.split(':')
    except ValueError:
        raise InvalidSearchQuery('Invalid reference event')
    try:
        project = Project.objects.get(slug=project_slug, organization=reference_event.organization, status=ProjectStatus.VISIBLE)
    except Project.DoesNotExist:
        raise InvalidSearchQuery('Invalid reference event')
    column_names = [resolve_column(col) for col in reference_event.fields if is_real_column(col)]
    if (not column_names):
        return None
    event = raw_query(selected_columns=column_names, filter_keys={
        'project_id': [project.id],
        'event_id': [event_id],
    }, dataset=Dataset.Discover, limit=1)
    if (('error' in event) or (len(event['data']) != 1)):
        raise InvalidSearchQuery('Invalid reference event')
    return event['data'][0]
