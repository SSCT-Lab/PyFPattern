def prepare_saml_request(self, request):
    url = urlparse(options.get('system.url-prefix'))
    return {
        'https': ('on' if (url.scheme == 'https') else 'off'),
        'http_host': url.hostname,
        'script_name': request.META['PATH_INFO'],
        'server_port': url.port,
        'get_data': request.GET.copy(),
        'post_data': request.POST.copy(),
    }