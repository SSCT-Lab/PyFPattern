def create_userreport(self, **kwargs):
    userreport = UserReport.objects.create(group=kwargs['group'], event_id=('a' * 32), project=kwargs['project'], name='Jane Doe', email='jane@example.com', comments=make_sentence())
    return userreport