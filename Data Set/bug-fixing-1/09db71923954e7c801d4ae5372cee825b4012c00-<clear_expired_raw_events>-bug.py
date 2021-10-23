

@instrumented_task(name='sentry.tasks.clear_expired_raw_events', time_limit=15, soft_time_limit=10)
def clear_expired_raw_events():
    from sentry.models import RawEvent, ProcessingIssue, ReprocessingReport
    cutoff = (timezone.now() - timedelta(days=settings.SENTRY_RAW_EVENT_MAX_AGE_DAYS))
    RawEvent.objects.filter(datetime__lt=cutoff).delete()
    ReprocessingReport.objects.filter(datetime__lt=cutoff).delete()
    cutoff = (timezone.now() - timedelta(days=int((settings.SENTRY_RAW_EVENT_MAX_AGE_DAYS * 1.3))))
    ProcessingIssue.objects.filter(datetime__lt=cutoff).delete()
