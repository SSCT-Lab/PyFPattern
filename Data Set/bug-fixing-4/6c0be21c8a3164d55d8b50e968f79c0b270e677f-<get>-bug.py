def get(self, request, sentry_app):
    if (not features.has('organizations:internal-catchall', sentry_app.owner)):
        return Response(status=404)
    return Response(serialize(sentry_app, request.user))