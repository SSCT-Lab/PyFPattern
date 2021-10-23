def _query(self, project, retention_window_start, group_queryset, tags, environment, sort_by, limit, cursor, count_hits, paginator_options, **parameters):
    from sentry.models import Group, Environment, Event, GroupEnvironment, Release
    if (environment is not None):
        if ('environment' in tags):
            environment_name = tags.pop('environment')
            assert ((environment_name is ANY) or (Environment.objects.get(projects=project, name=environment_name).id == environment.id))
        event_queryset_builder = QuerySetBuilder({
            'date_from': ScalarCondition('date_added', 'gt'),
            'date_to': ScalarCondition('date_added', 'lt'),
        })
        if any(((key in parameters) for key in event_queryset_builder.conditions.keys())):
            event_queryset = event_queryset_builder.build(tagstore.get_event_tag_qs(project_id=project.id, environment_id=environment.id, key='environment', value=environment.name), parameters)
            if (retention_window_start is not None):
                event_queryset = event_queryset.filter(date_added__gte=retention_window_start)
            group_queryset = group_queryset.filter(id__in=list(event_queryset.distinct().values_list('group_id', flat=True)[:1000]))
        group_queryset = QuerySetBuilder({
            'first_release': CallbackCondition((lambda queryset, version: queryset.extra(where=['{} = {}'.format(get_sql_column(GroupEnvironment, 'first_release_id'), get_sql_column(Release, 'id')), '{} = %s'.format(get_sql_column(Release, 'organization')), '{} = %s'.format(get_sql_column(Release, 'version'))], params=[project.organization_id, version], tables=[Release._meta.db_table]))),
            'times_seen': CallbackCondition((lambda queryset, times_seen: queryset.exclude(times_seen__lt=times_seen))),
            'times_seen_lower': CallbackCondition((lambda queryset, times_seen: queryset.exclude(times_seen__lt=times_seen))),
            'age_from': CallbackCondition((lambda queryset, first_seen: queryset.exclude(last_seen__lt=first_seen))),
            'age_to': CallbackCondition((lambda queryset, first_seen: queryset.exclude(first_seen__gt=first_seen))),
            'last_seen_from': CallbackCondition((lambda queryset, last_seen: queryset.exclude(last_seen__lt=last_seen))),
            'last_seen_to': CallbackCondition((lambda queryset, last_seen: queryset.exclude(first_seen__gt=last_seen))),
        }).build(group_queryset.extra(where=['{} = {}'.format(get_sql_column(Group, 'id'), get_sql_column(GroupEnvironment, 'group_id')), '{} = %s'.format(get_sql_column(GroupEnvironment, 'environment_id'))], params=[environment.id], tables=[GroupEnvironment._meta.db_table]), parameters)
        (get_sort_expression, sort_value_to_cursor_value) = environment_sort_strategies[sort_by]
        group_tag_value_queryset = tagstore.get_group_tag_value_qs(project_id=project.id, group_id=set(group_queryset.values_list('id', flat=True)[:10000]), environment_id=environment.id, key='environment', value=environment.name)
        if (retention_window_start is not None):
            group_tag_value_queryset = group_tag_value_queryset.filter(last_seen__gte=retention_window_start)
        candidates = dict(QuerySetBuilder({
            'age_from': ScalarCondition('first_seen', 'gt'),
            'age_to': ScalarCondition('first_seen', 'lt'),
            'last_seen_from': ScalarCondition('last_seen', 'gt'),
            'last_seen_to': ScalarCondition('last_seen', 'lt'),
            'times_seen': CallbackCondition((lambda queryset, times_seen: queryset.filter(times_seen=times_seen))),
            'times_seen_lower': ScalarCondition('times_seen', 'gt'),
            'times_seen_upper': ScalarCondition('times_seen', 'lt'),
        }).build(group_tag_value_queryset, parameters).extra(select={
            'sort_value': get_sort_expression(group_tag_value_queryset.model),
        }).values_list('group_id', 'sort_value'))
        if tags:
            matches = tagstore.get_group_ids_for_search_filter(project_id=project.id, environment_id=environment.id, tags=tags, candidates=candidates.keys(), limit=len(candidates))
            for key in (set(candidates) - set((matches or []))):
                del candidates[key]
        result = SequencePaginator([(sort_value_to_cursor_value(score), id) for (id, score) in candidates.items()], reverse=True, **paginator_options).get_result(limit, cursor, count_hits=count_hits)
        groups = Group.objects.in_bulk(result.results)
        result.results = [groups[k] for k in result.results if (k in groups)]
        return result
    else:
        event_queryset_builder = QuerySetBuilder({
            'date_from': ScalarCondition('datetime', 'gt'),
            'date_to': ScalarCondition('datetime', 'lt'),
        })
        if any(((key in parameters) for key in event_queryset_builder.conditions.keys())):
            group_queryset = group_queryset.filter(id__in=list(event_queryset_builder.build(Event.objects.filter(project_id=project.id), parameters).distinct().values_list('group_id', flat=True)[:1000]))
        group_queryset = QuerySetBuilder({
            'first_release': CallbackCondition((lambda queryset, version: queryset.filter(first_release__organization_id=project.organization_id, first_release__version=version))),
            'age_from': ScalarCondition('first_seen', 'gt'),
            'age_to': ScalarCondition('first_seen', 'lt'),
            'last_seen_from': ScalarCondition('last_seen', 'gt'),
            'last_seen_to': ScalarCondition('last_seen', 'lt'),
            'times_seen': CallbackCondition((lambda queryset, times_seen: queryset.filter(times_seen=times_seen))),
            'times_seen_lower': ScalarCondition('times_seen', 'gt'),
            'times_seen_upper': ScalarCondition('times_seen', 'lt'),
        }).build(group_queryset, parameters).extra(select={
            'sort_value': get_sort_clause(sort_by),
        })
        if tags:
            group_ids = tagstore.get_group_ids_for_search_filter(project_id=project.id, environment_id=None, tags=tags, candidates=None)
            if group_ids:
                group_queryset = group_queryset.filter(id__in=group_ids)
            else:
                group_queryset = group_queryset.none()
        (paginator_cls, sort_clause) = sort_strategies[sort_by]
        group_queryset = group_queryset.order_by(sort_clause)
        paginator = paginator_cls(group_queryset, sort_clause, **paginator_options)
        return paginator.get_result(limit, cursor, count_hits=count_hits)