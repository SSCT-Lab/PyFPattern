def get_multi(self, id_list):
    if (self.thread_pool is None):
        return super(BigtableNodeStorage, self).get_multi(id_list)
    if (len(id_list) == 1):
        id = id_list[0]
        return {
            id: self.get(id),
        }
    return {id: data for (id, data) in izip(id_list, self.thread_pool.map(self.get, id_list))}