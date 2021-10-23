@never_cache
@transaction.atomic
def handle(self, request):
    if (not request.user.is_authenticated()):
        return self.handle_auth_required(request)
    if (request.POST.get('op') == 'confirm'):
        request.user.update(is_active=True)
        return self.redirect(auth.get_login_redirect(request))
    context = {
        
    }
    return self.respond('sentry/reactivate-account.html', context)