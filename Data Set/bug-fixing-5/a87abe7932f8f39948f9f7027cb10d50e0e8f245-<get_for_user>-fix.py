def get_for_user(self, user, scope=None, only_visible=True):
    '\n        Returns a set of all organizations a user has access to.\n        '
    from sentry.models import OrganizationMember
    if (not user.is_authenticated()):
        return []
    if (settings.SENTRY_PUBLIC and (scope is None)):
        if only_visible:
            return list(self.filter(status=OrganizationStatus.VISIBLE))
        else:
            return list(self.filter())
    qs = OrganizationMember.objects.filter(user=user).select_related('organization')
    if only_visible:
        qs = qs.filter(organization__status=OrganizationStatus.VISIBLE)
    results = list(qs)
    if (scope is not None):
        return [r.organization for r in results if (scope in r.get_scopes())]
    return [r.organization for r in results]