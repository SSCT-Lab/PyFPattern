def post(self, request, organization):
    '\n        Add a invite request to Organization\n        ````````````````````````````````````\n\n        Creates an invite request given an email and sugested role / teams.\n\n        :pparam string organization_slug: the slug of the organization the member will belong to\n        :param string email: the email address to invite\n        :param string role: the suggested role of the new member\n        :param array teams: the suggested slugs of the teams the member should belong to.\n\n        :auth: required\n        '
    variant = experiments.get(org=organization, experiment_name='ImprovedInvitesExperiment')
    if (variant not in ('all', 'invite_request')):
        return Response(status=403)
    serializer = OrganizationMemberSerializer(data=request.data, context={
        'organization': organization,
        'allowed_roles': roles.get_all(),
    })
    if (not serializer.is_valid()):
        return Response(serializer.errors, status=400)
    result = serializer.validated_data
    with transaction.atomic():
        om = OrganizationMember.objects.create(organization=organization, email=result['email'], role=result['role'], inviter=request.user, invite_status=InviteStatus.REQUESTED_TO_BE_INVITED.value)
        if result['teams']:
            lock = locks.get('org:member:{}'.format(om.id), duration=5)
            with TimedRetryPolicy(10)(lock.acquire):
                save_team_assignments(om, result['teams'])
        self.create_audit_entry(request=request, organization_id=organization.id, target_object=om.id, data=om.get_audit_log_data(), event=AuditLogEntryEvent.INVITE_REQUEST_ADD)
    om.send_request_notification_email()
    return Response(serialize(om), status=201)