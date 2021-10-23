def handle(self, request):
    user = auth.get_pending_2fa_user(request)
    if (user is None):
        return HttpResponseRedirect(auth.get_login_url())
    interfaces = Authenticator.objects.all_interfaces_for_user(user)
    if (not interfaces):
        return self.perform_signin(request, user)
    challenge = activation = None
    interface = self.negotiate_interface(request, interfaces)
    if ((request.method == 'POST') and ratelimiter.is_limited('auth-2fa:user:{}'.format(user.id), limit=5, window=60)):
        return HttpResponse('You have made too many 2FA attempts. Please try again later.', content_type='text/plain', status=429)
    if (request.method == 'GET'):
        activation = interface.activate(request)
        if ((activation is not None) and (activation.type == 'challenge')):
            challenge = activation.challenge
    elif ('challenge' in request.POST):
        challenge = json.loads(request.POST['challenge'])
    form = TwoFactorForm()
    otp = request.POST.get('otp')
    if otp:
        used_interface = self.validate_otp(otp, interface, interfaces)
        if (used_interface is not None):
            return self.perform_signin(request, user, used_interface)
        self.fail_signin(request, user, form)
    if challenge:
        response = request.POST.get('response')
        if response:
            response = json.loads(response)
            if interface.validate_response(request, challenge, response):
                return self.perform_signin(request, user, interface)
            self.fail_signin(request, user, form)
    return render_to_response([('sentry/twofactor_%s.html' % interface.interface_id), 'sentry/twofactor.html'], {
        'form': form,
        'interface': interface,
        'other_interfaces': self.get_other_interfaces(interface, interfaces),
        'activation': activation,
    }, request, status=200)