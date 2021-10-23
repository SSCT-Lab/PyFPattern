@require_GET
def generate_all_emails(request: HttpRequest) -> HttpResponse:
    if (not settings.TEST_SUITE):
        subprocess.check_call(['./tools/inline-email-css'])
    from django.test import Client
    client = Client()
    registered_email = 'hamlet@zulip.com'
    unregistered_email_1 = 'new-person@zulip.com'
    unregistered_email_2 = 'new-person-2@zulip.com'
    realm = get_realm('zulip')
    host_kwargs = {
        'HTTP_HOST': realm.host,
    }
    result = client.post('/accounts/password/reset/', {
        'email': registered_email,
    }, **host_kwargs)
    assert (result.status_code == 302)
    result = client.post('/accounts/home/', {
        'email': unregistered_email_1,
    }, **host_kwargs)
    assert (result.status_code == 302)
    result = client.post('/accounts/find/', {
        'emails': registered_email,
    }, **host_kwargs)
    assert (result.status_code == 302)
    logged_in = client.login(dev_auth_username=registered_email, realm=realm)
    assert logged_in
    result = client.post('/json/invites', {
        'invitee_emails': unregistered_email_2,
        'stream': ['Denmark'],
    }, **host_kwargs)
    assert (result.status_code == 200)
    result = client.patch('/json/settings', urllib.parse.urlencode({
        'email': 'hamlets-new@zulip.com',
    }), **host_kwargs)
    assert (result.status_code == 200)
    key = Confirmation.objects.filter(type=Confirmation.EMAIL_CHANGE).latest('id').confirmation_key
    url = confirmation_url(key, realm.host, Confirmation.EMAIL_CHANGE)
    user_profile = get_user_by_delivery_email(registered_email, realm)
    result = client.get(url)
    assert (result.status_code == 200)
    user_profile.email = registered_email
    user_profile.save(update_fields=['email'])
    enqueue_welcome_emails(user_profile)
    enqueue_welcome_emails(get_user_by_delivery_email('iago@zulip.com', realm), realm_creation=True)
    return redirect(email_page)