def has_release_permission(self, request, organization, release):
    '\n        Does the given request have permission to access this release, based\n        on the projects to which the release is attached?\n\n        If the given request has an actor (user or ApiKey), cache the results\n        for a minute on the unique combination of actor,org,release.\n        '
    actor_id = None
    has_perms = None
    if (getattr(request, 'user', None) and request.user.id):
        actor_id = ('user:%s' % request.user.id)
    if (getattr(request, 'auth', None) and request.auth.id):
        actor_id = ('apikey:%s' % request.auth.id)
    if (actor_id is not None):
        key = ('release_perms:1:%s' % hash_values([actor_id, organization.id, release.id]))
        has_perms = cache.get(key)
    if (has_perms is None):
        has_perms = ReleaseProject.objects.filter(release=release, project__in=self.get_projects(request, organization)).exists()
        if (actor_id is not None):
            cache.set(key, has_perms, 60)
    return has_perms