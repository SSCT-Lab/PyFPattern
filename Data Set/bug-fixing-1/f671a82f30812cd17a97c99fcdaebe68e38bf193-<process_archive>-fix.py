

def process_archive(members, zip, sdk_info, threads=8, trim_symbols=False, demangle=True):
    from sentry.models import DSymSymbol
    import Queue
    q = Queue.Queue(threads)

    def process_items():
        while 1:
            items = q.get()
            if (items is SHUTDOWN):
                break
            DSymSymbol.objects.bulk_insert(items)
    pool = []
    for x in xrange(threads):
        t = threading.Thread(target=process_items)
        t.setDaemon(True)
        t.start()
        pool.append(t)
    for member in members:
        try:
            id = uuid.UUID(member)
        except ValueError:
            continue
        for chunk in load_bundle(q.put, id, json.load(zip.open(member)), sdk_info, trim_symbols, demangle):
            q.put(chunk)
    for t in pool:
        q.put(SHUTDOWN)
    for t in pool:
        t.join()
