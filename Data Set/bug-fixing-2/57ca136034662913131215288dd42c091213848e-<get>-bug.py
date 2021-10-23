

@attach_scenarios([list_organization_projects_scenario])
def get(self, request, organization):
    "\n        List an Organization's Projects\n        ```````````````````````````````\n\n        Return a list of projects bound to a organization.\n\n        :pparam string organization_slug: the slug of the organization for\n                                          which the projects should be listed.\n        :auth: required\n        "
    stats_period = request.GET.get('statsPeriod')
    if (stats_period not in (None, '', '24h', '14d', '30d')):
        return Response({
            'error': {
                'params': {
                    'stats_period': {
                        'message': ERR_INVALID_STATS_PERIOD,
                    },
                },
            },
        }, status=400)
    elif (not stats_period):
        stats_period = None
    if (request.auth and (not request.user.is_authenticated())):
        if hasattr(request.auth, 'project'):
            team_list = list(request.auth.project.teams.all())
            queryset = Project.objects.filter(id=request.auth.project.id).prefetch_related('teams')
        elif (request.auth.organization is not None):
            org = request.auth.organization
            team_list = list(Team.objects.filter(organization=org))
            queryset = Project.objects.filter(teams__in=team_list).prefetch_related('teams')
        else:
            return Response({
                'detail': 'Current access does not point to organization.',
            }, status=400)
    else:
        team_list = list(request.access.teams)
        queryset = Project.objects.filter(teams__in=team_list).prefetch_related('teams')
    query = request.GET.get('query')
    if query:
        tokens = tokenize_query(query)
        for (key, value) in six.iteritems(tokens):
            if (key == 'query'):
                value = ' '.join(value)
                queryset = queryset.filter((Q(name__icontains=value) | Q(slug__icontains=value)))
            else:
                queryset = queryset.none()
    queryset = queryset.distinct()
    return self.paginate(request=request, queryset=queryset, order_by='slug', on_results=(lambda x: serialize(x, request.user, ProjectSummarySerializer(environment_id=self._get_environment_id_from_request(request, organization.id), stats_period=stats_period))), paginator_cls=OffsetPaginator)
