def resolve_actors(owners, project_id):
    ' Convert a list of Owner objects into a dictionary\n    of {Owner: Actor} pairs. Actors not identified are returned\n    as None. '
    from sentry.api.fields.actor import Actor
    from sentry.ownership.grammar import Owner
    from sentry.models import User, Team
    if (not owners):
        return {
            
        }
    (users, teams) = ([], [])
    owners_to_actors = {o: None for o in owners}
    for owner in owners:
        if (owner.type == 'user'):
            users.append(owner)
        elif (owner.type == 'team'):
            teams.append(owner)
    actors = []
    if users:
        actors.extend([('user', email, Actor(u_id, User)) for (u_id, email) in User.objects.filter(reduce(operator.or_, [Q(email__iexact=o.identifier) for o in users]), is_active=True, sentry_orgmember_set__organizationmemberteam__team__projectteam__project_id=project_id).values_list('id', 'email')])
    if teams:
        actors.extend([('team', slug, Actor(t_id, Team)) for (t_id, slug) in Team.objects.filter(slug__in=[o.identifier for o in teams], projectteam__project_id=project_id).values_list('id', 'slug')])
    for (type, identifier, actor) in actors:
        owners_to_actors[Owner(type, identifier)] = actor
    return owners_to_actors