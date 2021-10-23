def get(self, request, organization):
    if (not features.has('organizations:events-v2', organization, actor=request.user)):
        return Response(status=404)
    try:
        params = self.get_filter_params(request, organization)
        snuba_args = self.get_snuba_query_args(request, organization, params)
    except OrganizationEventsError as exc:
        return Response({
            'detail': exc.message,
        }, status=400)
    except NoProjects:
        return Response({
            'detail': 'A valid project must be included.',
        }, status=400)
    try:
        key = self._validate_key(request)
        self._validate_project_ids(request, organization, snuba_args)
    except OrganizationEventsError as error:
        return Response({
            'detail': six.text_type(error),
        }, status=400)
    colname = get_snuba_column_name(key)
    if (key == PROJECT_KEY):
        colname = 'project_id'
    top_values = raw_query(start=snuba_args['start'], end=snuba_args['end'], conditions=(snuba_args['conditions'] + [[colname, 'IS NOT NULL', None]]), filter_keys=snuba_args['filter_keys'], groupby=[colname], aggregations=[('count()', None, 'count')], orderby='-count', limit=TOP_VALUES_DEFAULT_LIMIT, referrer='api.organization-events-distribution')['data']
    projects = {p.id: p.slug for p in self.get_projects(request, organization)}
    if (key == PROJECT_KEY):
        resp = {
            'key': PROJECT_KEY,
            'topValues': [{
                'value': projects[v['project_id']],
                'name': projects[v['project_id']],
                'count': v['count'],
            } for v in top_values],
        }
    else:
        resp = {
            'key': key,
            'topValues': [{
                'value': v[colname],
                'name': tagstore.get_tag_value_label(colname, v[colname]),
                'count': v['count'],
            } for v in top_values],
        }
    return Response(resp)