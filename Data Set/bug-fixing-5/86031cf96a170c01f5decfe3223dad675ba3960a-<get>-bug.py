def get(self, request, organization, version):
    "\n        List an Organization Release's Commits\n        ``````````````````````````````````````\n\n        Retrieve a list of commits for a given release.\n\n        :pparam string organization_slug: the slug of the organization the\n                                          release belongs to.\n        :pparam string version: the version identifier of the release.\n        :auth: required\n        "
    try:
        release = Release.objects.get(organization_id=organization.id, projects__in=self.get_allowed_projects(request, organization), version=version)
    except Release.DoesNotExist:
        raise ResourceDoesNotExist
    queryset = ReleaseCommit.objects.filter(release=release).select_related('commit', 'commit__author')
    return self.paginate(request=request, queryset=queryset, order_by='order', on_results=(lambda x: serialize([rc.commit for rc in x], request.user)))