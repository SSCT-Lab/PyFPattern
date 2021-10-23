def get_generic_get_iter(self, call, attribute=None, field=None, query=None, children='attributes-list'):
    generic_call = self.call_api(call, query)
    if (field is None):
        out = []
    else:
        out = {
            
        }
    attributes_list = generic_call.get_child_by_name(children)
    if (attributes_list is None):
        return None
    for child in attributes_list.get_children():
        d = xmltodict.parse(child.to_string(), xml_attribs=False)
        if (attribute is not None):
            d = d[attribute]
        if isinstance(field, str):
            unique_key = _finditem(d, field)
            out = out.copy()
            out.update({
                unique_key: convert_keys(json.loads(json.dumps(d))),
            })
        elif isinstance(field, tuple):
            unique_key = ':'.join([_finditem(d, el) for el in field])
            out = out.copy()
            out.update({
                unique_key: convert_keys(json.loads(json.dumps(d))),
            })
        else:
            out.append(convert_keys(json.loads(json.dumps(d))))
    return out