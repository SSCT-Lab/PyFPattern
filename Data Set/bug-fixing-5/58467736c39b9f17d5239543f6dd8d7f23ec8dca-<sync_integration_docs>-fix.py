def sync_integration_docs(platform_id, integration_id, path, quiet=False):
    if (not quiet):
        echo(('  syncing documentation for %s.%s integration' % (platform_id, integration_id)))
    data = json.load(urlopen_with_retries(BASE_URL.format(path)))
    key = get_integration_id(platform_id, integration_id)
    dump_doc(key, {
        'id': key,
        'name': data['name'],
        'html': data['body'],
        'link': data['doc_link'],
    })