def run_symbolicator(project, request_id_cache_key, create_task=create_payload_task, **kwargs):
    symbolicator_options = options.get('symbolicator.options')
    base_url = symbolicator_options['url'].rstrip('/')
    assert base_url
    project_id = six.text_type(project.id)
    request_id = default_cache.get(request_id_cache_key)
    sess = Session()
    sources = None
    attempts = 0
    wait = 0.5
    with sess:
        while True:
            try:
                if request_id:
                    rv = _poll_symbolication_task(sess=sess, base_url=base_url, request_id=request_id, project_id=project_id)
                else:
                    if (sources is None):
                        sources = get_sources_for_project(project)
                    rv = create_task(sess=sess, base_url=base_url, project_id=project_id, sources=sources, **kwargs)
                metrics.incr('events.symbolicator.status_code', tags={
                    'status_code': rv.status_code,
                    'project_id': project_id,
                })
                if ((rv.status_code == 404) and request_id):
                    default_cache.delete(request_id_cache_key)
                    request_id = None
                    continue
                elif (rv.status_code == 503):
                    raise RetrySymbolication(retry_after=10)
                rv.raise_for_status()
                json = rv.json()
                metrics.incr('events.symbolicator.response', tags={
                    'response': json['status'],
                    'project_id': project_id,
                })
                if (json['status'] == 'pending'):
                    default_cache.set(request_id_cache_key, json['request_id'], REQUEST_CACHE_TIMEOUT)
                    raise RetrySymbolication(retry_after=json['retry_after'])
                elif (json['status'] == 'completed'):
                    default_cache.delete(request_id_cache_key)
                    return rv.json()
                else:
                    logger.error('Unexpected status: %s', json['status'])
                    default_cache.delete(request_id_cache_key)
                    return
            except (IOError, RequestException):
                attempts += 1
                if (attempts > MAX_ATTEMPTS):
                    logger.error('Failed to contact symbolicator', exc_info=True)
                    default_cache.delete(request_id_cache_key)
                    return
                time.sleep(wait)
                wait *= 2.0