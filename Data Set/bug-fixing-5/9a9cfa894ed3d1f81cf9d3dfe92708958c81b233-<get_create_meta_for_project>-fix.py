def get_create_meta_for_project(self, project):
    params = {
        'expand': 'projects.issuetypes.fields',
        'projectIds': project,
    }
    metas = self.get_cached(self.META_URL, params=params)
    if (not metas):
        logger.info('jira.get-create-meta.empty-response', extra={
            'base_url': self.base_url,
            'project': project,
        })
        return None
    if (len(metas['projects']) > 1):
        raise ApiError('More than one project found matching {}.'.format(project))
    try:
        return metas['projects'][0]
    except IndexError:
        logger.info('jira.get-create-meta.key-error', extra={
            'base_url': self.base_url,
            'project': project,
        })
        return None