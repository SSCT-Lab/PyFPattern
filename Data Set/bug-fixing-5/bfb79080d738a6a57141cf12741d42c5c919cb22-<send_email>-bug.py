@instrumented_task(name='sentry.tasks.email.send_email', queue='email', default_retry_delay=(60 * 5), max_retries=None)
def send_email(message):
    send_messages([message])