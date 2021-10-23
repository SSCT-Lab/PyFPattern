def has_release_permission(self, request, organization, release):
    return ReleaseProject.objects.filter(release=release, project__in=self.get_projects(request, organization)).exists()