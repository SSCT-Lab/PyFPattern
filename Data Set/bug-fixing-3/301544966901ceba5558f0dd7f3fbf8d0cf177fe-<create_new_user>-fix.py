@requires_admin
@transaction.atomic
@csrf_protect
def create_new_user(request):
    if (not request.is_superuser()):
        return HttpResponseRedirect(get_login_url())
    form = NewUserForm((request.POST or None), initial={
        'send_welcome_mail': True,
        'create_project': True,
    })
    if form.is_valid():
        user = form.save(commit=False)
        password = uuid.uuid4().hex
        user.set_password(password)
        user.save()
        if form.cleaned_data['send_welcome_mail']:
            context = {
                'username': user.username,
                'password': password,
                'url': absolute_uri(get_login_url()),
            }
            body = render_to_string('sentry/emails/welcome_mail.txt', context, request)
            try:
                send_mail(('%s Welcome to Sentry' % (options.get('mail.subject-prefix'),)), body, options.get('mail.from'), [user.email], fail_silently=False)
            except Exception as e:
                logger = logging.getLogger('sentry.mail.errors')
                logger.exception(e)
        return HttpResponseRedirect(absolute_uri('/manage/users/'))
    context = {
        'form': form,
    }
    context.update(csrf(request))
    return render_to_response('sentry/admin/users/new.html', context, request)