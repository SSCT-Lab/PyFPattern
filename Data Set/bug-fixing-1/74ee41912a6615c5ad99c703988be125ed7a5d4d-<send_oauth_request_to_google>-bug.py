

def send_oauth_request_to_google(request: HttpRequest) -> HttpResponse:
    subdomain = request.GET.get('subdomain', '')
    is_signup = request.GET.get('is_signup', '')
    next = request.GET.get('next', '')
    mobile_flow_otp = request.GET.get('mobile_flow_otp', '0')
    if ((settings.ROOT_DOMAIN_LANDING_PAGE and (subdomain == '')) or (not Realm.objects.filter(string_id=subdomain).exists())):
        return redirect_to_subdomain_login_url()
    google_uri = 'https://accounts.google.com/o/oauth2/auth?'
    cur_time = str(int(time.time()))
    csrf_state = ('%s:%s:%s:%s:%s' % (cur_time, subdomain, mobile_flow_otp, is_signup, next))
    csrf_state += (':%s' % (google_oauth2_csrf(request, csrf_state),))
    params = {
        'response_type': 'code',
        'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
        'redirect_uri': reverse_on_root('zerver.views.auth.finish_google_oauth2'),
        'scope': 'profile email',
        'state': csrf_state,
    }
    return redirect((google_uri + urllib.parse.urlencode(params)))
