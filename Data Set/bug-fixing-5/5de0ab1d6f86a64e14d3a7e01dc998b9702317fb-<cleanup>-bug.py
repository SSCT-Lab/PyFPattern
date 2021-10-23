@click.command()
@click.option('--days', default=30, show_default=True, help='Numbers of days to truncate on.')
@click.option('--project', help='Limit truncation to only entries from project.')
@click.option('--concurrency', type=int, default=1, show_default=True, help='The number of concurrent workers to run.')
@click.option('--silent', '-q', default=False, is_flag=True, help='Run quietly. No output on success.')
@click.option('--model', '-m', multiple=True)
@click.option('--router', '-r', default=None, help='Database router')
@click.option('--timed', '-t', default=False, is_flag=True, help='Send the duration of this command to internal metrics.')
@log_options()
@configuration
def cleanup(days, project, concurrency, silent, model, router, timed):
    'Delete a portion of trailing data based on creation date.\n\n    All data that is older than `--days` will be deleted.  The default for\n    this is 30 days.  In the default setting all projects will be truncated\n    but if you have a specific project you want to limit this to this can be\n    done with the `--project` flag which accepts a project ID or a string\n    with the form `org/project` where both are slugs.\n    '
    if (concurrency < 1):
        click.echo('Error: Minimum concurrency is 1', err=True)
        raise click.Abort()
    from threading import Thread
    from django.db import router as db_router
    from sentry.app import nodestore
    from sentry.db.deletion import BulkDeleteQuery
    from sentry import deletions
    from sentry import models
    if timed:
        import time
        from sentry.utils import metrics
        start_time = time.time()
    model_list = {m.lower() for m in model}

    def is_filtered(model):
        if ((router is not None) and (db_router.db_for_write(model) != router)):
            return True
        if (not model_list):
            return False
        return (model.__name__.lower() not in model_list)
    BULK_QUERY_DELETES = ((models.GroupEmailThread, 'date', None), (models.GroupRuleStatus, 'date_added', None), (models.GroupTagValue, 'last_seen', None), (models.TagValue, 'last_seen', None), (models.EventTag, 'date_added', 'date_added'))
    DELETES = ((models.Event, 'datetime', None), (models.Group, 'last_seen', 'last_seen'))
    if (not silent):
        click.echo('Removing expired values for LostPasswordHash')
    if is_filtered(models.LostPasswordHash):
        if (not silent):
            click.echo('>> Skipping LostPasswordHash')
    else:
        models.LostPasswordHash.objects.filter(date_added__lte=(timezone.now() - timedelta(hours=48))).delete()
    for model in [models.ApiGrant, models.ApiToken]:
        if (not silent):
            click.echo('Removing expired values for {}'.format(model.__name__))
        if is_filtered(model):
            if (not silent):
                click.echo('>> Skipping {}'.format(model.__name__))
        else:
            model.objects.filter(expires_at__lt=timezone.now()).delete()
    project_id = None
    if project:
        click.echo('Bulk NodeStore deletion not available for project selection', err=True)
        project_id = get_project(project)
        if (project_id is None):
            click.echo('Error: Project not found', err=True)
            raise click.Abort()
    elif (not silent):
        click.echo('Removing old NodeStore values')
    else:
        cutoff = (timezone.now() - timedelta(days=days))
        try:
            nodestore.cleanup(cutoff)
        except NotImplementedError:
            click.echo('NodeStore backend does not support cleanup operation', err=True)
    for (model, dtfield, order_by) in BULK_QUERY_DELETES:
        if (not silent):
            click.echo('Removing {model} for days={days} project={project}'.format(model=model.__name__, days=days, project=(project or '*')))
        if is_filtered(model):
            if (not silent):
                click.echo(('>> Skipping %s' % model.__name__))
        else:
            BulkDeleteQuery(model=model, dtfield=dtfield, days=days, project_id=project_id, order_by=order_by).execute()
    for (model, dtfield, order_by) in DELETES:
        if (not silent):
            click.echo('Removing {model} for days={days} project={project}'.format(model=model.__name__, days=days, project=(project or '*')))
        if is_filtered(model):
            if (not silent):
                click.echo(('>> Skipping %s' % model.__name__))
        else:
            query = {
                '{}__lte'.format(dtfield): (timezone.now() - timedelta(days=days)),
            }
            if project_id:
                if ('project' in model._meta.get_all_field_names()):
                    query['project'] = project_id
                else:
                    query['project_id'] = project_id
            task = deletions.get(model=model, query=query, order_by=order_by, transaction_id=uuid4().hex)

            def _chunk_until_complete(num_shards=None, shard_id=None):
                has_more = True
                while has_more:
                    has_more = task.chunk(num_shards=num_shards, shard_id=shard_id)
            if (concurrency > 1):
                threads = []
                for shard_id in range(concurrency):
                    t = Thread(target=(lambda shard_id=shard_id: _chunk_until_complete(num_shards=concurrency, shard_id=shard_id)))
                    t.start()
                    threads.append(t)
                for t in threads:
                    t.join()
            else:
                _chunk_until_complete()
    if (not silent):
        click.echo('Removing expired values for EventMapping')
    if is_filtered(models.EventMapping):
        if (not silent):
            click.echo('>> Skipping EventMapping')
    else:
        BulkDeleteQuery(model=models.EventMapping, dtfield='date_added', days=min(days, 7), project_id=project_id, order_by='-date_added').execute()
    if (not silent):
        click.echo('Cleaning up unused FileBlob references')
    if is_filtered(models.FileBlob):
        if (not silent):
            click.echo('>> Skipping FileBlob')
    else:
        cleanup_unused_files(silent)
    if timed:
        duration = int((time.time() - start_time))
        metrics.timing('cleanup.duration', duration, instance=router)
        click.echo(('Clean up took %s second(s).' % duration))