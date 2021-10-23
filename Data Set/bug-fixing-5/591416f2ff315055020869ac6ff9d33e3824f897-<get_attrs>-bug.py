def get_attrs(self, item_list, user):
    tag_labels = {t.key: t.get_label() for t in TagKey.objects.filter(project_id=item_list[0].project.id, key__in=[i.key for i in item_list])}
    result = {
        
    }
    for item in item_list:
        key = TagKey.get_standardized_key(item.key)
        try:
            label = tag_labels[item.key]
        except KeyError:
            label = key
        result[item] = {
            'name': label,
            'key': key,
        }
    return result