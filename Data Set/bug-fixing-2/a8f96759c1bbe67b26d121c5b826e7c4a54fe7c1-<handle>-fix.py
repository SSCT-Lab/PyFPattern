

def handle(self, *args: Any, **options: Any) -> None:
    if settings.EMAIL_DELIVERER_DISABLED:
        time.sleep((10 ** 9))
    with lockfile('/tmp/zulip_email_deliver.lockfile'):
        while True:
            email_jobs_to_deliver = ScheduledEmail.objects.filter(scheduled_timestamp__lte=timezone_now())
            if email_jobs_to_deliver:
                for job in email_jobs_to_deliver:
                    try:
                        send_email(**loads(job.data))
                        job.delete()
                    except EmailNotDeliveredException:
                        logger.warning(('%r not delivered' % (job,)))
                time.sleep(10)
            else:
                time.sleep(2)
