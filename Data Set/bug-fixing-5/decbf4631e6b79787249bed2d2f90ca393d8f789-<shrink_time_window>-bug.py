def shrink_time_window(issues, start):
    "    If a single issue is passed in, shrink the `start` parameter to be briefly before\n    the `first_seen` in order to hopefully eliminate a large percentage of rows scanned.\n\n    Note that we don't shrink `end` based on `last_seen` because that value is updated\n    asynchronously by buffers, and will cause queries to skip recently seen data on\n    stale groups.\n    "
    if (issues and (len(issues) == 1)):
        group = Group.objects.get(pk=issues[0])
        start = max(start, (naiveify_datetime(group.first_seen) - timedelta(minutes=5)))
    return start