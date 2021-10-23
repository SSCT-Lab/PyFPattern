def merge_objects(models, group, new_group, limit=1000, logger=None, transaction_id=None):
    from sentry.models import GroupTagKey, GroupTagValue
    has_more = False
    for model in models:
        all_fields = model._meta.get_all_field_names()
        has_group = ('group' in all_fields)
        if has_group:
            queryset = model.objects.filter(group=group)
        else:
            queryset = model.objects.filter(group_id=group.id)
        for obj in queryset[:limit]:
            try:
                with transaction.atomic(using=router.db_for_write(model)):
                    if has_group:
                        model.objects.filter(id=obj.id).update(group=new_group)
                    else:
                        model.objects.filter(id=obj.id).update(group_id=new_group.id)
            except IntegrityError:
                delete = True
            else:
                delete = False
            if delete:
                try:
                    if (model == GroupTagKey):
                        with transaction.atomic(using=router.db_for_write(model)):
                            model.objects.filter(group=new_group, key=obj.key).update(values_seen=GroupTagValue.objects.filter(group_id=new_group.id, key=obj.key).count())
                    elif (model == GroupTagValue):
                        with transaction.atomic(using=router.db_for_write(model)):
                            new_obj = model.objects.get(group_id=new_group.id, key=obj.key, value=obj.value)
                            new_obj.update(first_seen=min(new_obj.first_seen, obj.first_seen), last_seen=max(new_obj.last_seen, obj.last_seen), times_seen=(new_obj.times_seen + obj.times_seen))
                except DataError:
                    pass
                obj_id = obj.id
                obj.delete()
                if (logger is not None):
                    delete_logger.debug('object.delete.executed', extra={
                        'object_id': obj_id,
                        'transaction_id': transaction_id,
                        'model': model.__name__,
                    })
            has_more = True
        if has_more:
            return True
    return has_more