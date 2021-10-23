def handle_api_error(self, error):
    context = {
        'error_type': 'unknown',
    }
    if isinstance(error, InvalidIdentity):
        context.update({
            'error_type': 'auth',
            'auth_url': reverse('socialauth_associate', args=[self.auth_provider]),
        })
        status = 400
    elif isinstance(error, PluginError):
        context.update({
            'error_type': 'validation',
            'errors': {
                '__all__': error.message,
            },
        })
        status = 400
    else:
        if self.logger:
            self.logger.exception(six.text_type(error))
        status = 500
    return Response(context, status=status)