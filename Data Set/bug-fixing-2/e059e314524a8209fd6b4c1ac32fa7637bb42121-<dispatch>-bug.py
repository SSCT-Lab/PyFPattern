

@csrf_exempt
def dispatch(self, request, *args, **kwargs):
    if self.csrf_protect:
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
