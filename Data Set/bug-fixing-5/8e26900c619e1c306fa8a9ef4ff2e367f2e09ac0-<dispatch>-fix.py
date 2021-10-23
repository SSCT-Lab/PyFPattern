@csrf_exempt
def dispatch(self, request, *args, **kwargs):
    "\n        Identical to rest framework's dispatch except we add the ability\n        to convert arguments (for common URL params).\n        "
    self.args = args
    self.kwargs = kwargs
    request = self.initialize_request(request, *args, **kwargs)
    self.request = request
    self.headers = self.default_response_headers
    if settings.SENTRY_API_RESPONSE_DELAY:
        time.sleep((settings.SENTRY_API_RESPONSE_DELAY / 1000.0))
    origin = request.META.get('HTTP_ORIGIN', 'null')
    if (origin == 'null'):
        origin = None
    try:
        if (origin and request.auth):
            allowed_origins = request.auth.get_allowed_origins()
            if (not is_valid_origin(origin, allowed=allowed_origins)):
                response = Response(('Invalid origin: %s' % (origin,)), status=400)
                self.response = self.finalize_response(request, response, *args, **kwargs)
                return self.response
        self.initial(request, *args, **kwargs)
        if (getattr(request, 'user', None) and request.user.is_authenticated()):
            raven.user_context({
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
            })
        if (request.method.lower() in self.http_method_names):
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            (args, kwargs) = self.convert_args(request, *args, **kwargs)
            self.args = args
            self.kwargs = kwargs
        else:
            handler = self.http_method_not_allowed
        response = handler(request, *args, **kwargs)
    except Exception as exc:
        response = self.handle_exception(request, exc)
    if origin:
        self.add_cors_headers(request, response)
    self.response = self.finalize_response(request, response, *args, **kwargs)
    return self.response