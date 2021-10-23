

def on_delete(instance, actor=None, **kwargs):

    def handle_exception(exc):
        from sentry.exceptions import InvalidIdentity, PluginError
        from sentry.integrations.exceptions import IntegrationError
        if isinstance(exc, (IntegrationError, PluginError, InvalidIdentity)):
            error = exc.message
        else:
            error = 'An unknown error occurred'
        if (actor is not None):
            msg = instance.generate_delete_fail_email(error)
            msg.send_async(to=[actor.email])
    if instance.has_integration_provider():
        try:
            instance.get_provider().delete_repository(repo=instance)
        except Exception as exc:
            handle_exception(exc)
    else:
        try:
            instance.get_provider().delete_repository(repo=instance, actor=actor)
        except Exception as exc:
            handle_exception(exc)
