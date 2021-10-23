

def get_child_relations(self, instance):
    from sentry import models
    relations = super(EventDeletionTask, self).get_child_relations(instance)
    relations.extend([ModelRelation(models.EventAttachment, {
        'event_id': instance.event_id,
    }), ModelRelation(models.EventMapping, {
        'event_id': instance.event_id,
    }), ModelRelation(models.UserReport, {
        'event_id': instance.event_id,
    })])
    return relations
