@csrf_exempt
def dispatch(self, request, *args, **kwargs):
    "\n        A note on the CSRF protection process.\n\n        Because the CSRF decorators don't work well with view subclasses, we\n        allow them to control whether a CSRF check is done by setting\n        self.csrf_protect. This has a couple of implications:\n\n        1. We need to mark this method as @csrf_exempt so that when the CSRF\n           middleware checks it as part of the regular middleware sequence, it\n           always passes.\n        2. If self.csrf_protect is set, we will re-run the CSRF check ourselves\n           using CsrfViewMiddleware().process_view()\n        3. But first we must remove the csrf_exempt attribute that was set by\n           the decorator so that the middleware doesn't shortcut and pass the\n           check unconditionally again.\n\n        "
    if self.csrf_protect:
        if hasattr(self.dispatch.__func__, 'csrf_exempt'):
            delattr(self.dispatch.__func__, 'csrf_exempt')
        response = self.test_csrf(request)
        if response:
            return response
    if self.is_auth_required(request, *args, **kwargs):
        return self.handle_auth_required(request, *args, **kwargs)
    if self.is_sudo_required(request, *args, **kwargs):
        return self.handle_sudo_required(request, *args, **kwargs)
    (args, kwargs) = self.convert_args(request, *args, **kwargs)
    request.access = self.get_access(request, *args, **kwargs)
    if (not self.has_permission(request, *args, **kwargs)):
        return self.handle_permission_required(request, *args, **kwargs)
    self.request = request
    self.default_context = self.get_context_data(request, *args, **kwargs)
    return self.handle(request, *args, **kwargs)