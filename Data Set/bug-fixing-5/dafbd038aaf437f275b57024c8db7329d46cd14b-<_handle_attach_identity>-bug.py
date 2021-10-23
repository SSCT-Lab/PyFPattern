@transaction.atomic
def _handle_attach_identity(self, identity, member=None):
    '\n        Given an already authenticated user, attach or re-attach and identity.\n        '
    auth_provider = self.auth_provider
    request = self.request
    user = request.user
    organization = self.organization
    try:
        try:
            auth_identity = AuthIdentity.objects.get(auth_provider=auth_provider, ident=identity['id'])
        except AuthIdentity.DoesNotExist:
            auth_identity = AuthIdentity.objects.get(auth_provider=auth_provider, user=user)
    except AuthIdentity.DoesNotExist:
        auth_identity = AuthIdentity.objects.create(auth_provider=auth_provider, user=user, ident=identity['id'], data=identity.get('data', {
            
        }))
        auth_is_new = True
    else:
        now = timezone.now()
        auth_identity.update(user=user, ident=identity['id'], data=self.provider.update_identity(new_data=identity.get('data', {
            
        }), current_data=auth_identity.data), last_verified=now, last_synced=now)
        auth_is_new = False
    if (member is None):
        try:
            member = OrganizationMember.objects.get(user=user, organization=organization)
        except OrganizationMember.DoesNotExist:
            member = OrganizationMember.objects.create(organization=organization, role=organization.default_role, user=user, flags=getattr(OrganizationMember.flags, 'sso:linked'))
            default_teams = auth_provider.default_teams.all()
            for team in default_teams:
                OrganizationMemberTeam.objects.create(team=team, organizationmember=member)
            AuditLogEntry.objects.create(organization=organization, actor=user, ip_address=request.META['REMOTE_ADDR'], target_object=member.id, target_user=user, event=AuditLogEntryEvent.MEMBER_ADD, data=member.get_audit_log_data())
    if (getattr(member.flags, 'sso:invalid') or (not getattr(member.flags, 'sso:linked'))):
        setattr(member.flags, 'sso:invalid', False)
        setattr(member.flags, 'sso:linked', True)
        member.save()
    if auth_is_new:
        AuditLogEntry.objects.create(organization=organization, actor=user, ip_address=request.META['REMOTE_ADDR'], target_object=auth_identity.id, event=AuditLogEntryEvent.SSO_IDENTITY_LINK, data=auth_identity.get_audit_log_data())
        messages.add_message(request, messages.SUCCESS, OK_LINK_IDENTITY)
    return auth_identity