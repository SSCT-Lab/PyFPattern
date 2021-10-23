def delete_multi(self, id_list):
    if self.skip_deletes:
        return
    if (self.thread_pool is None):
        return super(BigtableNodeStorage, self).delete_multi(id_list)
    if (len(id_list) == 1):
        self.delete(id_list[0])
        return
    for _ in self.thread_pool.map(self.delete, id_list):
        pass