def fetch_system_symbols(self, processing_task):
    to_lookup = []
    pf_list = []
    for pf in processing_task.iter_processable_frames(self):
        obj = pf.data['obj']
        if ((pf.cache_value is not None) or (obj is None) or self.sym.is_image_from_app_bundle(obj)):
            continue
        to_lookup.append({
            'object_uuid': six.text_type(obj.uuid),
            'object_name': (obj.name or '<unknown>'),
            'addr': ('0x%x' % rebase_addr(pf.data['instruction_addr'], obj)),
        })
        pf_list.append(pf)
    if (not to_lookup):
        return
    rv = lookup_system_symbols(to_lookup, self.sdk_info, self.arch)
    if (rv is not None):
        for (symrv, pf) in zip(rv, pf_list):
            if (symrv is None):
                continue
            pf.data['symbolserver_match'] = symrv