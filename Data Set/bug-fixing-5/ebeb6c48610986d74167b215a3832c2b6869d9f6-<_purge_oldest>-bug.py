@staticmethod
def _purge_oldest(category, maxpurge=1):
    print('PURGE', category)
    import heapq
    heap_list = []
    for key in Cache._objects[category]:
        obj = Cache._objects[category][key]
        if (obj['lastaccess'] == obj['timestamp']):
            continue
        heapq.heappush(heap_list, (obj['lastaccess'], key))
        print('<<<', obj['lastaccess'])
    n = 0
    while (n < maxpurge):
        try:
            (lastaccess, key) = heapq.heappop(heap_list)
            print('=>', key, lastaccess, Clock.get_time())
        except Exception:
            return
        del Cache._objects[category][key]