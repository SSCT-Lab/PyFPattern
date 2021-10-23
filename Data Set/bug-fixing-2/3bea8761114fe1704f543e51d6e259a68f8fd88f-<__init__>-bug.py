

def __init__(self):
    super(ImportAddedPlugin, self).__init__()
    self.config.add({
        'preserve_mtimes': False,
        'preserve_write_mtimes': False,
    })
    self.reimported_item_ids = None
    self.replaced_album_paths = None
    self.item_mtime = dict()
    register = self.register_listener
    register('import_task_start', self.check_config)
    register('import_task_start', self.record_if_inplace)
    register('import_task_files', self.record_reimported)
    register('before_item_moved', self.record_import_mtime)
    register('item_copied', self.record_import_mtime)
    register('item_linked', self.record_import_mtime)
    register('item_hardlinked', self.record_import_mtime)
    register('album_imported', self.update_album_times)
    register('item_imported', self.update_item_times)
    register('after_write', self.update_after_write_time)
