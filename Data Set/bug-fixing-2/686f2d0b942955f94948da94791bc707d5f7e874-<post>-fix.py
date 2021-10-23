

def post(self, request, organization):
    if (not features.has('organizations:discover', organization, actor=request.user)):
        return Response(status=404)
    try:
        requested_projects = set(map(int, request.data.get('projects', [])))
    except (ValueError, TypeError):
        raise ResourceDoesNotExist()
    projects = self._get_projects_by_id(requested_projects, request, organization)
    serializer = DiscoverQuerySerializer(data=request.data)
    if (not serializer.is_valid()):
        return Response(serializer.errors, status=400)
    serialized = serializer.validated_data
    has_aggregations = (len(serialized.get('aggregations')) > 0)
    selected_columns = ((serialized.get('conditionFields', []) + []) if has_aggregations else serialized.get('fields', []))
    projects_map = {
        
    }
    for project in projects:
        projects_map[project.id] = project.slug
    groupby = (serialized.get('groupby') or [])
    fields = (serialized.get('fields') or [])
    if has_aggregations:
        for field in fields:
            if (field not in groupby):
                groupby.append(field)
    return self.do_query(projects=projects_map, start=serialized.get('start'), end=serialized.get('end'), groupby=groupby, selected_columns=selected_columns, conditions=serialized.get('conditions'), orderby=serialized.get('orderby'), limit=serialized.get('limit'), aggregations=serialized.get('aggregations'), rollup=serialized.get('rollup'), filter_keys={
        'project.id': projects_map.keys(),
    }, arrayjoin=serialized.get('arrayjoin'), request=request, turbo=serialized.get('turbo'))
