def post(self, request):
    if (not (is_active_superuser(request) and request.access.has_permission('broadcasts.admin'))):
        return self.respond(status=401)
    validator = AdminBroadcastValidator(data=request.DATA)
    if (not validator.is_valid()):
        return self.respond(validator.errors, status=400)
    result = validator.object
    with transaction.atomic():
        broadcast = Broadcast.objects.create(title=result['title'], message=result['message'], link=result['link'], is_active=(result.get('isActive') or False), date_expires=result.get('expiresAt'))
        logger.info('broadcasts.create', extra={
            'ip_address': request.META['REMOTE_ADDR'],
            'user_id': request.user.id,
            'broadcast_id': broadcast.id,
        })
    if result.get('hasSeen'):
        try:
            with transaction.atomic():
                BroadcastSeen.objects.create(broadcast=broadcast, user=request.user)
        except IntegrityError:
            pass
    return self.respond(self._serialize_objects(broadcast, request))