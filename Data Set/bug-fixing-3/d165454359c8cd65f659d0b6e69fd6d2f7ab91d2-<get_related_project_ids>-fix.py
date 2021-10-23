def get_related_project_ids(column, ids):
    '\n    Get the project_ids from a model that has a foreign key to project.\n    '
    mappings = {
        'issue': (Group, 'id', 'project_id'),
        'tags[sentry:release]': (ReleaseProject, 'release_id', 'project_id'),
    }
    if ids:
        if (column == 'project_id'):
            return ids
        elif (column in mappings):
            (model, id_field, project_field) = mappings[column]
            return model.objects.filter(**{
                (id_field + '__in'): ids,
                (project_field + '__isnull'): False,
            }).values_list(project_field, flat=True)
    return []