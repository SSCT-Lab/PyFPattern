def error(self, request, name, status=400):
    client_id = request.POST.get('client_id')
    redirect_uri = request.POST.get('redirect_uri')
    logging.error('oauth.token-error', extra={
        'error_name': name,
        'status': status,
        'client_id': client_id,
        'redirect_uri': redirect_uri,
    })
    return HttpResponse(json.dumps({
        'error': name,
    }), content_type='application/json', status=status)