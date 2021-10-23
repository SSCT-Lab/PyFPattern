def has_release_permission(self, request, organization, release):
    '\n        Does the given request have permission to access this release, based\n        on the projects to which the release is attached?\n        '
    return ReleaseProject.objects.filter(release=release, project__in=self.get_projects(request, organization)).exists()