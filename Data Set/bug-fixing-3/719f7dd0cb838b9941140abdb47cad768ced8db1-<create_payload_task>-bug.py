def create_payload_task(sess, base_url, project_id, sources, signal, stacktraces, modules):
    request = {
        'signal': signal,
        'sources': sources,
        'request': {
            'timeout': SYMBOLICATOR_TIMEOUT,
        },
        'stacktraces': stacktraces,
        'modules': modules,
    }
    url = '{base_url}/symbolicate?timeout={timeout}&scope={scope}'.format(base_url=base_url, timeout=SYMBOLICATOR_TIMEOUT, scope=project_id)
    return sess.post(url, json=request)