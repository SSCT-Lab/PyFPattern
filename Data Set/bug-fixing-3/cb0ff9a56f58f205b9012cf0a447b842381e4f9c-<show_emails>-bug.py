@csrf_protect
@never_cache
@login_required
def show_emails(request):
    user = request.user
    primary_email = user.emails.get(email=user.email)
    alt_emails = user.emails.all().exclude(email=primary_email.email)
    email_form = EmailForm(user, (request.POST or None), initial={
        'primary_email': primary_email.email,
    })
    if ('remove' in request.POST):
        email = request.POST.get('email')
        del_email = UserEmail.objects.filter(user=user, email=email)
        del_email.delete()
        return HttpResponseRedirect(request.path)
    if email_form.is_valid():
        old_email = user.email
        email_form.save()
        if (user.email != old_email):
            useroptions = UserOption.objects.filter(user=user, value=old_email)
            for option in useroptions:
                option.value = user.email
                option.save()
            UserEmail.objects.filter(user=user, email=old_email).delete()
            try:
                with transaction.atomic():
                    user_email = UserEmail.objects.create(user=user, email=user.email)
            except IntegrityError:
                pass
            else:
                user_email.set_hash()
                user_email.save()
            user.send_confirm_emails()
        alternative_email = email_form.cleaned_data['alt_email']
        if (alternative_email and (not UserEmail.objects.filter(user=user, email=alternative_email))):
            try:
                with transaction.atomic():
                    new_email = UserEmail.objects.create(user=user, email=alternative_email)
            except IntegrityError:
                pass
            else:
                new_email.set_hash()
                new_email.save()
            user.send_confirm_emails()
        messages.add_message(request, messages.SUCCESS, 'Your settings were saved.')
        return HttpResponseRedirect(request.path)
    context = csrf(request)
    context.update({
        'email_form': email_form,
        'primary_email': primary_email,
        'alt_emails': alt_emails,
        'page': 'emails',
        'AUTH_PROVIDERS': get_auth_providers(),
    })
    return render_to_response('sentry/account/emails.html', context, request)