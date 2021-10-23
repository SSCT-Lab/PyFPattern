@csrf_protect
@never_cache
@login_required
def show_emails(request):
    user = request.user
    emails = user.emails.all()
    email_form = EmailForm(user, (request.POST or None))
    primary_email = UserEmail.get_primary_email(user)
    alt_emails = emails.exclude(email=primary_email.email)
    if ('remove' in request.POST):
        email = request.POST.get('email')
        del_email = UserEmail.objects.filter(user=user, email=email)
        del_email.delete()
        logger.info('user.email.remove', extra={
            'user_id': user.id,
            'ip_address': request.META['REMOTE_ADDR'],
            'email': email,
        })
        user.clear_lost_passwords()
        return HttpResponseRedirect(request.path)
    if ('primary' in request.POST):
        new_primary = request.POST['new_primary_email'].lower().strip()
        if User.objects.filter((Q(email__iexact=new_primary) | Q(username__iexact=new_primary))).exclude(id=user.id).exists():
            messages.add_message(request, messages.ERROR, _('That email is already in use for another user'))
        elif (new_primary != user.email):
            new_primary_email = UserEmail.objects.get(user=user, email__iexact=new_primary)
            if (not new_primary_email.is_verified):
                messages.add_message(request, messages.ERROR, _('Cannot make an unverified address your primary email'))
                return HttpResponseRedirect(request.path)
            alert_email = UserOption.objects.get_value(user=user, key='alert_email')
            if (alert_email == user.email):
                UserOption.objects.set_value(user=user, key='alert_email', value=new_primary)
            options = UserOption.objects.filter(user=user, key='mail:email')
            for option in options:
                if (option.value != user.email):
                    continue
                option.value = new_primary
                option.save()
            has_new_username = (user.email == user.username)
            user.email = new_primary
            msg = _('Your settings were saved')
            messages.add_message(request, messages.SUCCESS, msg)
            if (has_new_username and (not User.objects.filter(username__iexact=new_primary).exists())):
                user.username = user.email
            user.save()
        user.clear_lost_passwords()
        return HttpResponseRedirect(request.path)
    if email_form.is_valid():
        alternative_email = email_form.cleaned_data['alt_email'].lower().strip()
        if (alternative_email and (not UserEmail.objects.filter(user=user, email__iexact=alternative_email).exists())):
            try:
                with transaction.atomic():
                    new_email = UserEmail.objects.create(user=user, email=alternative_email)
            except IntegrityError:
                pass
            else:
                new_email.set_hash()
                new_email.save()
                user.send_confirm_email_singular(new_email)
                logger.info('user.email.add', extra={
                    'user_id': user.id,
                    'ip_address': request.META['REMOTE_ADDR'],
                    'email': new_email.email,
                })
                msg = (_('A confirmation email has been sent to %s.') % new_email.email)
                messages.add_message(request, messages.SUCCESS, msg)
        user.clear_lost_passwords()
        messages.add_message(request, messages.SUCCESS, _('Your settings were saved.'))
        return HttpResponseRedirect(request.path)
    context = csrf(request)
    context.update({
        'email_form': email_form,
        'primary_email': primary_email,
        'alt_emails': alt_emails,
        'page': 'emails',
        'AUTH_PROVIDERS': auth.get_auth_providers(),
        'has_newsletters': newsletter.is_enabled,
    })
    return render_to_response('sentry/account/emails.html', context, request)