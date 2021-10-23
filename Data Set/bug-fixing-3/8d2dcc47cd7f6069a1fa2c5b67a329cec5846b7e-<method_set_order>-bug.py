def method_set_order(self, ordered_obj, id_list, using=None):
    if (using is None):
        using = DEFAULT_DB_ALIAS
    order_wrt = ordered_obj._meta.order_with_respect_to
    filter_args = order_wrt.get_forward_related_filter(self)
    with transaction.atomic(using=using, savepoint=False):
        for (i, j) in enumerate(id_list):
            ordered_obj.objects.filter(pk=j, **filter_args).update(_order=i)