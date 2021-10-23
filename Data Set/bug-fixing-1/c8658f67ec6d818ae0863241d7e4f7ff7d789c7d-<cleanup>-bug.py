

@click.command()
@click.option('--days', default=30, show_default=True, help='Numbers of days to truncate on.')
@click.option('--project', help='Limit truncation to only entries from project.')
@click.option('--concurrency', type=int, default=1, show_default=True, help='The total number of concurrent threads to run across processes.')
@click.option('--max_procs', type=int, default=8, show_default=True, help='The maximum number of processes to fork off for concurrency.')
@click.option('--silent', '-q', default=False, is_flag=True, help='Run quietly. No output on success.')
@click.option('--model', '-m', multiple=True)
@click.option('--router', '-r', default=None, help='Database router')
@click.option('--timed', '-t', default=False, is_flag=True, help='Send the duration of this command to internal metrics.')
@log_options()
@configuration
def cleanup(days, project, concurrency, max_procs, silent, model, router, timed):
    'Delete a portion of trailing data based on creation date.\n\n    All data that is older than `--days` will be deleted.  The default for\n    this is 30 days.  In the default setting all projects will be truncated\n    but if you have a specific project you want to limit this to this can be\n    done with the `--project` flag which accepts a project ID or a string\n    with the form `org/project` where both are slugs.\n    '
    if (concurrency < 1):
        click.echo('Error: Minimum concurrency is 1', err=True)
        raise click.Abort()
    import math
    import multiprocessing
    import pickle
    import subprocess
    import sys
    from django.db import router as db_router
    from sentry.app import nodestore
    from sentry.db.deletion import BulkDeleteQuery
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
    BULK_QUERY_DELETES = ([(models.EventMapping, 'date_added', '-date_added'), (models.GroupHashTombstone, 'deleted_at', None), (models.GroupEmailThread, 'date', None), (models.GroupRuleStatus, 'date_added', None)] + EXTRA_BULK_QUERY_DELETES)
    DELETES = ((models.Event, 'datetime', 'datetime'), (models.Group, 'last_seen', 'last_seen'))
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
    for bqd in BULK_QUERY_DELETES:
        if (len(bqd) == 4):
            (model, dtfield, order_by, chunk_size) = bqd
        else:
            chunk_size = 10000
            (model, dtfield, order_by) = bqd
        if (not silent):
            click.echo('Removing {model} for days={days} project={project}'.format(model=model.__name__, days=days, project=(project or '*')))
        if is_filtered(model):
            if (not silent):
                click.echo(('>> Skipping %s' % model.__name__))
        else:
            BulkDeleteQuery(model=model, dtfield=dtfield, days=days, project_id=project_id, order_by=order_by).execute(chunk_size=chunk_size)
    for (model, dtfield, order_by) in DELETES:
        if (not silent):
            click.echo('Removing {model} for days={days} project={project}'.format(model=model.__name__, days=days, project=(project or '*')))
        if is_filtered(model):
            if (not silent):
                click.echo(('>> Skipping %s' % model.__name__))
        elif (concurrency > 1):
            shard_ids = range(concurrency)
            num_procs = min(multiprocessing.cpu_count(), max_procs)
            threads_per_proc = int(math.ceil((concurrency / float(num_procs))))
            pids = []
            for shard_id_chunk in chunker(shard_ids, threads_per_proc):
                pid = subprocess.Popen((([sys.argv[0], 'cleanup_chunk', '--days', six.binary_type(days)] + (['--project_id', six.binary_type(project_id)] if project_id else [])) + ['--model', pickle.dumps(model), '--dtfield', dtfield, '--order_by', order_by, '--num_shards', six.binary_type(concurrency), '--shard_ids', ','.join([six.binary_type(s) for s in shard_id_chunk])]))
                pids.append(pid)
            total_pid_count = len(pids)
            click.echo(('%s concurrent processes forked, waiting on them to complete.' % total_pid_count))
            complete = 0
            for pid in pids:
                pid.wait()
                complete += 1
                click.echo(('%s/%s concurrent processes are finished.' % (complete, total_pid_count)))
        else:
            task = create_deletion_task(days, project_id, model, dtfield, order_by)
            _chunk_until_complete(task)
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
