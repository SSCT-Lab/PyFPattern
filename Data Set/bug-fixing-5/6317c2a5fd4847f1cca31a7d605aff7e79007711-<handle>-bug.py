def handle(self, request):
    email = request.POST['user']
    try:
        user = User.objects.get(email__iexact=email, sentry_orgmember_set__organization__project=self.project)
    except (User.DoesNotExist, User.MultipleObjectsReturned):
        user = None
    self.finish_release(version=request.POST['head_long'], url=request.POST['url'], owner=user)