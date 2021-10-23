

def get_child_relations(self, instance):
    from sentry import models
    relations = super(EventDeletionTask, self).get_child_relations(instance)
    key = {
        'project_id': instance.project_id,
        'event_id': instance.event_id,
    }
    relations.extend([ModelRelation(models.EventAttachment, key), ModelRelation(models.EventMapping, key), ModelRelation(models.UserReport, key)])
    return relations
