def get_provider(organization_slug):
    try:
        organization = Organization.objects.get(slug=organization_slug)
    except Organization.DoesNotExist:
        return None
    if (organization.status != OrganizationStatus.VISIBLE):
        return None
    try:
        auth_provider = AuthProvider.objects.get(organization=organization)
        return auth_provider.get_provider()
    except AuthProvider.DoesNotExist:
        return None