

def update_subscriptions():
    try:
        f = open(options.stream_file_path, 'r')
        public_streams = simplejson.loads(f.read())
        f.close()
    except Exception:
        logger.exception('Error reading public streams:')
        return
    classes_to_subscribe = set()
    for stream in public_streams:
        zephyr_class = stream.encode('utf-8')
        if ((options.shard is not None) and (not hashlib.sha1(zephyr_class).hexdigest().startswith(options.shard))):
            continue
        if (zephyr_class in current_zephyr_subs):
            continue
        classes_to_subscribe.add((zephyr_class, '*', '*'))
    if (len(classes_to_subscribe) > 0):
        zephyr_bulk_subscribe(list(classes_to_subscribe))
