

@csrf_exempt
@login_required
@dsa_view()
def complete(request, backend, *args, **kwargs):
    'Authentication complete process'
    redirect_value = request.session.get(REDIRECT_FIELD_NAME, '')
    backend_name = backend.AUTH_BACKEND.name
    try:
        user = auth_complete(request, backend, request.user, *args, **kwargs)
    except AuthAlreadyAssociated:
        messages.add_message(request, messages.ERROR, 'This {} identity is already associated with another account.'.format(settings.AUTH_PROVIDER_LABELS.get(backend_name, backend_name)))
    except AuthException as exc:
        messages.add_message(request, messages.ERROR, six.text_type(exc))
    else:
        messages.add_message(request, messages.SUCCESS, 'You have linked your account with {}.'.format(settings.AUTH_PROVIDER_LABELS.get(backend_name, backend_name)))
    if (not user):
        url = (redirect_value or ASSOCIATE_ERROR_URL or DEFAULT_REDIRECT)
    elif isinstance(user, HttpResponse):
        return user
    else:
        url = (redirect_value or backend_setting(backend, 'SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL') or DEFAULT_REDIRECT)
    return HttpResponseRedirect(url)
