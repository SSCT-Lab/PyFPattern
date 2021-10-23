def _poll_symbolication_task(sess, base_url, request_id, project_id):
    url = '{base_url}/requests/{request_id}?timeout={timeout}'.format(base_url=base_url, request_id=request_id, timeout=SYMBOLICATOR_TIMEOUT)
    return sess.get(url, headers=_get_default_headers(project_id))