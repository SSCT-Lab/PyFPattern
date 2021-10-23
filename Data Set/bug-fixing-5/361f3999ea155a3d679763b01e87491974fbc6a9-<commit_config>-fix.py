def commit_config(self, comment=None, confirm=None):
    try:
        kwargs = dict(comment=comment)
        if (confirm and (confirm > 0)):
            kwargs['confirm'] = confirm
        return self.config.commit(**kwargs)
    except CommitError:
        exc = get_exception()
        raise NetworkError(('unable to commit config: %s' % str(exc)))