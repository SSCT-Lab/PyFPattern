

@csrf_protect
@never_cache
@login_required
@transaction.atomic
def settings(request):
    user = request.user
    form = AccountSettingsForm(user, (request.POST or None), initial={
        'email': user.email,
        'username': user.username,
        'name': user.name,
    })
    if form.is_valid():
        old_email = user.email
        form.save()
        if (request.user.email != old_email):
            UserEmail.objects.get(user=user, email=old_email).delete()
            try:
                with transaction.atomic():
                    user_email = UserEmail.objects.create(user=user, email=user.email)
            except IntegrityError:
                pass
            else:
                user_email.set_hash()
                user_email.save()
            user.send_confirm_emails()
        messages.add_message(request, messages.SUCCESS, 'Your settings were saved.')
        return HttpResponseRedirect(request.path)
    context = csrf(request)
    context.update({
        'form': form,
        'page': 'settings',
        'has_2fa': Authenticator.objects.user_has_2fa(request.user),
        'AUTH_PROVIDERS': get_auth_providers(),
    })
    return render_to_response('sentry/account/settings.html', context, request)
