def __class_prepared(self, sender, **kwargs):
    '\n        Given the cache is configured, connects the required signals for invalidation.\n        '
    post_save.connect(self.post_save, sender=sender, weak=False)
    post_delete.connect(self.post_delete, sender=sender, weak=False)
    if (not self.cache_fields):
        return
    post_init.connect(self.__post_init, sender=sender, weak=False)
    post_save.connect(self.__post_save, sender=sender, weak=False)
    post_delete.connect(self.__post_delete, sender=sender, weak=False)