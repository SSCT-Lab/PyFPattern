@classmethod
def get_or_create(cls, project, version, date_added):
    cache_key = cls.get_cache_key(project.id, version)
    release = cache.get(cache_key)
    if (release in (None, (- 1))):
        project_version = ('%s-%s' % (project.slug, version))[:64]
        releases = list(cls.objects.filter(organization_id=project.organization_id, version__in=[version, project_version], projects=project))
        if (len(releases) == 1):
            release = releases[0]
        elif (len(releases) > 1):
            release = [r for r in releases if (r.version == project_version)][0]
        else:
            release = cls.objects.filter(organization_id=project.organization_id, version=version).first()
            if (not release):
                lock_key = cls.get_lock_key(project.organization_id, version)
                lock = locks.get(lock_key, duration=5)
                with TimedRetryPolicy(10)(lock.acquire):
                    try:
                        release = cls.objects.get(organization_id=project.organization_id, version=version)
                    except cls.DoesNotExist:
                        release = cls.objects.create(organization_id=project.organization_id, version=version, date_added=date_added)
            release.add_project(project)
        cache.set(cache_key, release, 3600)
    return release