def load_user_conf(self, request):
    if (not request.user.is_authenticated()):
        return
    language = UserOption.objects.get_value(user=request.user, key='language')
    if language:
        request.session[LANGUAGE_SESSION_KEY] = language
    timezone = UserOption.objects.get_value(user=request.user, key='timezone')
    if timezone:
        request.timezone = pytz.timezone(timezone)