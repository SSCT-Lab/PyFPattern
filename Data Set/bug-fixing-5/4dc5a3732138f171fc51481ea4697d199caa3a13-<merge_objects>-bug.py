def merge_objects(models, group, new_group, limit=1000, logger=None, transaction_id=None):
    has_more = False
    for model in models:
        all_fields = [f.name for f in model._meta.get_fields()]
        has_project = (('project_id' in all_fields) or ('project' in all_fields))
        if (has_project and (model.__name__ != 'Event')):
            project_qs = model.objects.filter(project_id=group.project_id)
        else:
            project_qs = model.objects.all()
        has_group = ('group' in all_fields)
        if has_group:
            queryset = project_qs.filter(group=group)
        else:
            queryset = project_qs.filter(group_id=group.id)
        for obj in queryset[:limit]:
            if (has_project and (model.__name__ == 'Event') and (obj.project_id != group.project_id)):
                continue
            try:
                with transaction.atomic(using=router.db_for_write(model)):
                    if has_group:
                        project_qs.filter(id=obj.id).update(group=new_group)
                    else:
                        project_qs.filter(id=obj.id).update(group_id=new_group.id)
            except IntegrityError:
                delete = True
            else:
                delete = False
            if delete:
                if hasattr(model, 'merge_counts'):
                    obj.merge_counts(new_group)
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