def __search_events_snuba(self, request, project):
    from functools32 import partial
    from sentry.api.paginator import GenericOffsetPaginator
    from sentry.api.serializers.models.event import SnubaEvent
    from sentry.utils.snuba import raw_query
    query = request.GET.get('query')
    conditions = []
    if query:
        conditions.append([['positionCaseInsensitive', ['message', ("'%s'" % (query,))]], '!=', 0])
    now = timezone.now()
    data_fn = partial((lambda *args, **kwargs: raw_query(*args, **kwargs)['data']), start=(now - timedelta(days=90)), end=now, conditions=conditions, filter_keys={
        'project_id': [project.id],
    }, selected_columns=SnubaEvent.selected_columns, referrer='api.project-events')
    return self.paginate(request=request, on_results=(lambda results: serialize([SnubaEvent(row) for row in results], request.user)), paginator=GenericOffsetPaginator(data_fn=data_fn))