def setup_deletions(self, tagkey_model, tagvalue_model, grouptagkey_model, grouptagvalue_model, eventtag_model):
    from sentry.deletions import default_manager as deletion_manager
    from sentry.deletions.defaults import BulkModelDeletionTask, ModelDeletionTask
    from sentry.deletions.base import ModelRelation
    from sentry.models import Event, Group, Project
    deletion_manager.add_bulk_dependencies(Event, [(lambda instance_list: ModelRelation(eventtag_model, {
        'event_id__in': [i.id for i in instance_list],
        'project_id': instance_list[0].project_id,
    }, ModelDeletionTask))])
    deletion_manager.register(tagvalue_model, BulkModelDeletionTask)
    deletion_manager.register(grouptagkey_model, BulkModelDeletionTask)
    deletion_manager.register(grouptagvalue_model, BulkModelDeletionTask)
    deletion_manager.register(eventtag_model, BulkModelDeletionTask)
    deletion_manager.add_dependencies(Group, [(lambda instance: ModelRelation(eventtag_model, query={
        'group_id': instance.id,
        'project_id': instance.project_id,
    }, partition_key={
        'project_id': instance.project_id,
    })), (lambda instance: ModelRelation(grouptagkey_model, query={
        'group_id': instance.id,
        'project_id': instance.project_id,
    }, partition_key={
        'project_id': instance.project_id,
    })), (lambda instance: ModelRelation(grouptagvalue_model, query={
        'group_id': instance.id,
        'project_id': instance.project_id,
    }, partition_key={
        'project_id': instance.project_id,
    }))])
    deletion_manager.add_dependencies(Project, [(lambda instance: ModelRelation(tagkey_model, query={
        'project_id': instance.id,
    })), (lambda instance: ModelRelation(tagvalue_model, query={
        'project_id': instance.id,
    }, partition_key={
        'project_id': instance.id,
    })), (lambda instance: ModelRelation(grouptagkey_model, query={
        'project_id': instance.id,
    }, partition_key={
        'project_id': instance.id,
    })), (lambda instance: ModelRelation(grouptagvalue_model, query={
        'project_id': instance.id,
    }, partition_key={
        'project_id': instance.id,
    }))])