@instrumented_task(name='sentry.tasks.deletion.run_deletion', queue='cleanup', default_retry_delay=(60 * 5), max_retries=MAX_RETRIES)
@retry(exclude=(DeleteAborted,))
def run_deletion(deletion_id):
    from sentry import deletions
    from sentry.models import ScheduledDeletion
    try:
        deletion = ScheduledDeletion.objects.get(id=deletion_id)
    except ScheduledDeletion.DoesNotExist:
        return
    if deletion.aborted:
        raise DeleteAborted
    if (not deletion.in_progress):
        actor = deletion.get_actor()
        instance = deletion.get_instance()
        with transaction.atomc():
            deletion.update(in_progress=True)
            pending_delete.send(sender=type(instance), instance=instance, actor=actor)
    task = deletions.get(model=deletion.get_model(), query={
        'id': deletion.object_id,
    }, transaction_id=deletion.guid, actor_id=deletion.actor_id)
    has_more = task.chunk()
    if has_more:
        run_deletion.apply_async(kwargs={
            'deletion_id': deletion_id,
        }, countdown=15)
    deletion.delete()