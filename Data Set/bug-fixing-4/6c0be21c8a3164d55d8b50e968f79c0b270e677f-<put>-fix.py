def put(self, request, sentry_app):
    if (not features.has('organizations:internal-catchall', sentry_app.owner, actor=request.user)):
        return Response(status=404)
    serializer = SentryAppSerializer(data=request.DATA, partial=True)
    if serializer.is_valid():
        result = serializer.object
        updated_app = Updater.run(sentry_app=sentry_app, name=result.get('name'), webhook_url=result.get('webhookUrl'), redirect_url=result.get('redirectUrl'), is_alertable=result.get('isAlertable'), scopes=result.get('scopes'), overview=result.get('overview'))
        return Response(serialize(updated_app, request.user))
    return Response(serializer.errors, status=400)