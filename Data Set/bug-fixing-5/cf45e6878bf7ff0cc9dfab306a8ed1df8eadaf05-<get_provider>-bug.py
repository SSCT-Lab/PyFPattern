def get_provider(organization_slug):
    try:
        organization = Organization.objects.get(slug=organization_slug)
    except Organization.DoesNotExist:
        return HttpResponseRedirect(reverse('sentry-login'))
    if (organization.status != OrganizationStatus.VISIBLE):
        return HttpResponseRedirect(reverse('sentry-login'))
    try:
        auth_provider = AuthProvider.objects.get(organization=organization)
        return auth_provider.get_provider()
    except AuthProvider.DoesNotExist:
        return HttpResponseRedirect(reverse('sentry-login'))