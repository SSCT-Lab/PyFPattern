def prepare_project_series(start__stop, project, rollup=((60 * 60) * 24)):
    (start, stop) = start__stop
    (resolution, series) = tsdb.get_optimal_rollup_series(start, stop, rollup)
    assert (resolution == rollup), 'resolution does not match requested value'
    clean = functools.partial(clean_series, start, stop, rollup)
    return merge_series(reduce(merge_series, map(clean, tsdb.get_range(tsdb.models.group, list(project.group_set.filter(status=GroupStatus.RESOLVED, resolved_at__gte=start, resolved_at__lt=stop).values_list('id', flat=True)), start, stop, rollup=rollup).values()), clean([(timestamp, 0) for timestamp in series])), clean(tsdb.get_range(tsdb.models.project, [project.id], start, stop, rollup=rollup)[project.id]), (lambda resolved, total: (resolved, (total - resolved))))