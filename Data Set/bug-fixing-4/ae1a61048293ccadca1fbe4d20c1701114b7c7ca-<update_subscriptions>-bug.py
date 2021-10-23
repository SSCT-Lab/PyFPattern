def update_subscriptions(self, regexp):
    changed = False
    consumed_pools = RhsmPools(self.module, consumed=True)
    pool_ids_to_keep = [p.get_pool_id() for p in consumed_pools.filter(regexp)]
    serials_to_remove = [p.Serial for p in consumed_pools if (p.get_pool_id() not in pool_ids_to_keep)]
    serials = self.unsubscribe(serials=serials_to_remove)
    subscribed_pool_ids = self.subscribe(regexp)
    if (subscribed_pool_ids or serials):
        changed = True
    return {
        'changed': changed,
        'subscribed_pool_ids': subscribed_pool_ids,
        'unsubscribed_serials': serials,
    }