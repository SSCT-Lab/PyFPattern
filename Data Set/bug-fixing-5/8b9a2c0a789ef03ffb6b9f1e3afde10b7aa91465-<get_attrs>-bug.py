def get_attrs(self, item_list, user, *args, **kwargs):
    project = kwargs.get('project')
    if project:
        project_ids = [project.id]
    else:
        project_ids = ReleaseProject.objects.filter(release__in=item_list).values_list('project_id', flat=True)
    tags = {
        
    }
    tks = TagValue.objects.filter(project_id__in=project_ids, key='sentry:release', value__in=[o.version for o in item_list])
    for tk in tks:
        val = tags.get(tk.value)
        tags[tk.value] = {
            'first_seen': (min(tk.first_seen, val['first_seen']) if val else tk.first_seen),
            'last_seen': (max(tk.last_seen, val['last_seen']) if val else tk.last_seen),
        }
    owners = {d['id']: d for d in serialize(set((i.owner for i in item_list if i.owner_id)), user)}
    if project:
        group_counts_by_release = dict(ReleaseProject.objects.filter(project=project, release__in=item_list).values_list('release_id', 'new_groups'))
    else:
        group_counts_by_release = dict(ReleaseProject.objects.filter(release__in=item_list, new_groups__isnull=False).values('release_id').annotate(new_groups=Sum('new_groups')).values_list('release_id', 'new_groups'))
    release_metadata_attrs = self._get_commit_metadata(item_list, user)
    deploy_metadata_attrs = self._get_deploy_metadata(item_list, user)
    release_projects = defaultdict(list)
    project_releases = ReleaseProject.objects.filter(release__in=item_list).values('release_id', 'project__slug', 'project__name')
    for pr in project_releases:
        release_projects[pr['release_id']].append({
            'slug': pr['project__slug'],
            'name': pr['project__name'],
        })
    result = {
        
    }
    for item in item_list:
        result[item] = {
            'tag': tags.get(item.version),
            'owner': (owners[six.text_type(item.owner_id)] if item.owner_id else None),
            'new_groups': (group_counts_by_release.get(item.id) or 0),
            'projects': release_projects.get(item.id, []),
        }
        result[item].update(release_metadata_attrs[item])
        result[item].update(deploy_metadata_attrs[item])
    return result