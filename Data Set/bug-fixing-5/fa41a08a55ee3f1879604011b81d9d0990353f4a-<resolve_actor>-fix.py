def resolve_actor(owner, project_id):
    ' Convert an Owner object into an Actor '
    from sentry.api.fields.actor import Actor
    from sentry.models import User, Team
    if (owner.type == 'user'):
        try:
            user_id = User.objects.filter(email__iexact=owner.identifier, is_active=True, sentry_orgmember_set__organizationmemberteam__team__projectteam__project_id=project_id).values_list('id', flat=True)[0]
        except IndexError:
            raise UnknownActor
        return Actor(user_id, User)
    if (owner.type == 'team'):
        try:
            team_id = Team.objects.filter(projectteam__project_id=project_id, slug=owner.identifier).values_list('id', flat=True)[0]
        except IndexError:
            raise UnknownActor
        return Actor(team_id, Team)
    raise TypeError(('Unknown actor type: %r' % owner.type))