def check(self):
    if settings.CELERY_ALWAYS_EAGER:
        return []
    last_ping = (options.get('sentry:last_worker_ping') or 0)
    if (last_ping >= (time() - 300)):
        return []
    return [Problem("Background workers haven't checked in recently. This can mean an issue with your configuration or a serious backlog in tasks.", url=absolute_uri(reverse('sentry-admin-queue')))]