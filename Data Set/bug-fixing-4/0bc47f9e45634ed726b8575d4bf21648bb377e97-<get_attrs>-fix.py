def get_attrs(self, item_list, user, *args, **kwargs):
    environments = {id: name for (id, name) in Environment.objects.filter(id__in=[d.environment_id for d in item_list]).values_list('id', 'name')}
    result = {
        
    }
    for item in item_list:
        result[item] = {
            'environment': environments.get(item.environment_id),
        }
    return result