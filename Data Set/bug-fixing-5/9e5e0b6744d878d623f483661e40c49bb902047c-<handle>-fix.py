def handle(self, request, organization, team, project, group_id, slug):
    group = get_object_or_404(Group, pk=group_id, project=project)
    try:
        plugin = plugins.get(slug)
    except KeyError:
        raise Http404('Plugin not found')
    GroupMeta.objects.populate_cache([group])
    response = plugin.get_view_response(request, group)
    if response:
        return response
    redirect = request.META.get('HTTP_REFERER', '')
    if (not is_safe_url(redirect, host=request.get_host())):
        redirect = '/{}/{}/'.format(organization.slug, group.project.slug)
    return HttpResponseRedirect(redirect)