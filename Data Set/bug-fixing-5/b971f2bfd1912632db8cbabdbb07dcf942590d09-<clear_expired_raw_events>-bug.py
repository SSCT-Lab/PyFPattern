@instrumented_task(name='sentry.tasks.clear_expired_raw_events', time_limit=15, soft_time_limit=10)
def clear_expired_raw_events():
    from sentry.models import RawEvent, ProcessingIssue, ReprocessingReport

    def batched_delete(model_cls, **filter):
        while True:
            result = model_cls.objects.filter(**filter)[:200]
            if (not result.exists()):
                break
            model_cls.objects.filter(pk__in=result.values_list('pk')).delete()
    cutoff = (timezone.now() - timedelta(days=settings.SENTRY_RAW_EVENT_MAX_AGE_DAYS))
    batched_delete(RawEvent, datetime__lt=cutoff)
    batched_delete(ReprocessingReport, datetime__lt=cutoff)
    cutoff = (timezone.now() - timedelta(days=int((settings.SENTRY_RAW_EVENT_MAX_AGE_DAYS * 1.3))))
    batched_delete(ProcessingIssue, datetime__lt=cutoff)