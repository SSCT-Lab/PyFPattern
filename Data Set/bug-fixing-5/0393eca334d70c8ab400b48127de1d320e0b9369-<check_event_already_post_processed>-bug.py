def check_event_already_post_processed(event):
    cluster_key = getattr(settings, 'SENTRY_POST_PROCESSING_LOCK_REDIS_CLUSTER', None)
    if (cluster_key is None):
        return
    client = redis_clusters.get(cluster_key)
    result = client.set('pp:{}/{}'.format(event.project_id, event.event_id), '{:.0f}'.format(time.time()), ex=(60 * 60), nx=True)
    return (not result.value)