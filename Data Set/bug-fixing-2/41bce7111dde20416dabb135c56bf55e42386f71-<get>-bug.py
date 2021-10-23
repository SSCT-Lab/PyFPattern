

@attach_scenarios([list_project_issues_scenario])
def get(self, request, project):
    '\n        List a Project\'s Issues\n        ```````````````````````\n\n        Return a list of issues (groups) bound to a project.  All parameters are\n        supplied as query string parameters.\n\n        A default query of ``is:unresolved`` is applied. To return results\n        with other statuses send an new query value (i.e. ``?query=`` for all\n        results).\n\n        The ``statsPeriod`` parameter can be used to select the timeline\n        stats which should be present. Possible values are: \'\' (disable),\n        \'24h\', \'14d\'\n\n        :qparam string statsPeriod: an optional stat period (can be one of\n                                    ``"24h"``, ``"14d"``, and ``""``).\n        :qparam bool shortIdLookup: if this is set to true then short IDs are\n                                    looked up by this function as well.  This\n                                    can cause the return value of the function\n                                    to return an event issue of a different\n                                    project which is why this is an opt-in.\n                                    Set to `1` to enable.\n        :qparam querystring query: an optional Sentry structured search\n                                   query.  If not provided an implied\n                                   ``"is:unresolved"`` is assumed.)\n        :pparam string organization_slug: the slug of the organization the\n                                          issues belong to.\n        :pparam string project_slug: the slug of the project the issues\n                                     belong to.\n        :auth: required\n        '
    stats_period = request.GET.get('statsPeriod')
    if (stats_period not in (None, '', '24h', '14d')):
        return Response({
            'detail': ERR_INVALID_STATS_PERIOD,
        }, status=400)
    elif (stats_period is None):
        stats_period = '24h'
    elif (stats_period == ''):
        stats_period = None
    serializer = functools.partial(StreamGroupSerializer, environment_func=self._get_environment_func(request, project.organization_id), stats_period=stats_period)
    query = request.GET.get('query', '').strip()
    if query:
        matching_group = None
        matching_event = None
        event_id = normalize_event_id(query)
        if event_id:
            try:
                matching_group = Group.objects.from_event_id(project, event_id)
            except Group.DoesNotExist:
                pass
            else:
                matching_event = eventstore.get_event_by_id(project.id, event_id)
                if (matching_event is not None):
                    Event.objects.bind_nodes([matching_event], 'data')
        elif (matching_group is None):
            matching_group = get_by_short_id(project.organization_id, request.GET.get('shortIdLookup'), query)
            if ((matching_group is not None) and (matching_group.project_id != project.id)):
                matching_group = None
        if (matching_group is not None):
            matching_event_environment = None
            try:
                matching_event_environment = (matching_event.get_environment().name if matching_event else None)
            except Environment.DoesNotExist:
                pass
            response = Response(serialize([matching_group], request.user, serializer(matching_event_id=getattr(matching_event, 'id', None), matching_event_environment=matching_event_environment)))
            response['X-Sentry-Direct-Hit'] = '1'
            return response
    try:
        (cursor_result, query_kwargs) = self._search(request, project, {
            'count_hits': True,
        })
    except ValidationError as exc:
        return Response({
            'detail': six.text_type(exc),
        }, status=400)
    results = list(cursor_result)
    context = serialize(results, request.user, serializer())
    status = [search_filter for search_filter in query_kwargs.get('search_filters', []) if (search_filter.key.name == 'status')]
    if (status and (status[0].value.raw_value == GroupStatus.UNRESOLVED)):
        context = [r for r in context if (r['status'] == 'unresolved')]
    response = Response(context)
    self.add_cursor_headers(request, response, cursor_result)
    if (results and (query not in DEFAULT_SAVED_SEARCH_QUERIES)):
        advanced_search.send(project=project, sender=request.user)
        analytics.record('project_issue.searched', user_id=request.user.id, organization_id=project.organization_id, project_id=project.id, query=query)
    return response
