def setup_cleanup(self):
    from sentry.runner.commands import cleanup
    cleanup.EXTRA_BULK_QUERY_DELETES += [(models.GroupTagValue, 'last_seen', None), (models.TagValue, 'last_seen', None), (models.EventTag, 'date_added', 'date_added', 50000)]