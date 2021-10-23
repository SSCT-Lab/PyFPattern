def _forwards(self, orm):
    'Write your forwards methods here.'
    dupe_envs = orm.Environment.objects.values('name', 'organization_id').annotate(ecount=models.Count('id')).filter(ecount__gt=1)
    for env in dupe_envs:
        name = env['name']
        organization_id = env['organization_id']
        envs = list(orm.Environment.objects.filter(name=name, organization_id=organization_id).order_by('date_added'))
        to_env = envs[0]
        from_envs = envs[1:]
        try:
            with transaction.atomic():
                orm.EnvironmentProject.objects.filter(environment__in=from_envs).update(environment=to_env)
        except IntegrityError:
            for ep in orm.EnvironmentProject.objects.filter(environment__in=from_envs):
                try:
                    with transaction.atomic():
                        orm.EnvironmentProject.objects.filter(id=ep.id).update(environment=to_env)
                except IntegrityError:
                    ep.delete()
        from_env_ids = [e.id for e in from_envs]
        try:
            with transaction.atomic():
                orm.ReleaseEnvironment.objects.filter(environment_id__in=from_env_ids).update(environment_id=to_env.id)
        except IntegrityError:
            for re in orm.ReleaseEnvironment.objects.filter(environment_id__in=from_env_ids):
                try:
                    with transaction.atomic():
                        orm.ReleaseEnvironment.objects.filter(id=re.id).update(environment_id=to_env.id)
                except IntegrityError:
                    re.delete()
        orm.Environment.objects.filter(id__in=from_env_ids).delete()
    dupe_release_envs = orm.ReleaseEnvironment.objects.values('release_id', 'organization_id', 'environment_id').annotate(recount=models.Count('id')).filter(recount__gt=1)
    for renv in dupe_release_envs:
        release_id = renv['release_id']
        organization_id = renv['organization_id']
        environment_id = renv['environment_id']
        renvs = list(orm.ReleaseEnvironment.objects.filter(release_id=release_id, organization_id=organization_id, environment_id=environment_id).order_by('first_seen'))
        to_renv = renvs[0]
        from_renvs = renvs[1:]
        last_seen = max([re.last_seen for re in renvs])
        orm.ReleaseEnvironment.objects.filter(id=to_renv.id).update(last_seen=last_seen)
        orm.ReleaseEnvironment.objects.filter(id__in=[re.id for re in from_renvs]).delete()