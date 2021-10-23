def po_to_envra(po):
    if hasattr(po, 'ui_envra'):
        return po.ui_envra
    else:
        return ('%s:%s-%s-%s.%s' % (po.epoch, po.name, po.version, po.release, po.arch))