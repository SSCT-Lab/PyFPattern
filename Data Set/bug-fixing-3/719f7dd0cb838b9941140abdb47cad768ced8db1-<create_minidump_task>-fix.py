def create_minidump_task(sess, base_url, project_id, sources, minidump):
    files = {
        'upload_file_minidump': minidump,
    }
    data = {
        'sources': json.dumps(sources),
    }
    url = '{base_url}/minidump?timeout={timeout}&scope={scope}'.format(base_url=base_url, timeout=SYMBOLICATOR_TIMEOUT, scope=project_id)
    return sess.post(url, data=data, files=files, headers=_get_default_headers(project_id))