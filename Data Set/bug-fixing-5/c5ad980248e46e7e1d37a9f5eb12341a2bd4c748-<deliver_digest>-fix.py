@instrumented_task(name='sentry.tasks.digests.deliver_digest', queue='digests.delivery')
def deliver_digest(key, schedule_timestamp=None):
    from sentry import digests
    try:
        (plugin, project) = split_key(key)
    except Project.DoesNotExist as error:
        logger.info('Cannot deliver digest %r due to error: %s', key, error)
        digests.delete(key)
        return
    minimum_delay = ProjectOption.objects.get_value(project, get_option_key(plugin.get_conf_key(), 'minimum_delay'))
    with snuba.options_override({
        'consistent': True,
    }):
        try:
            with digests.digest(key, minimum_delay=minimum_delay) as records:
                digest = build_digest(project, records)
        except InvalidState as error:
            logger.info('Skipped digest delivery: %s', error, exc_info=True)
            return
        if digest:
            plugin.notify_digest(project, digest)