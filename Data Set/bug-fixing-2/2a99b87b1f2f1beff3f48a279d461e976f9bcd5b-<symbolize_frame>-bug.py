

def symbolize_frame(self, instruction_addr, sdk_info=None, symbolserver_match=None, symbolicator_match=None, trust=None):
    app_err = None
    if (symbolicator_match is None):
        obj = self.object_lookup.find_object(instruction_addr)
        if (obj is None):
            if (trust == 'scan'):
                return []
            raise SymbolicationFailed(type=EventError.NATIVE_UNKNOWN_IMAGE)
        try:
            match = self._symbolize_app_frame(instruction_addr, obj, sdk_info=sdk_info, trust=trust)
            if match:
                return match
        except SymbolicationFailed as err:
            app_err = err
    elif (all(((x['status'] == 'symbolicated') for x in symbolicator_match)) or (symbolicator_match == [])):
        return symbolicator_match
    match = self._convert_symbolserver_match(instruction_addr, symbolserver_match)
    if ((app_err is not None) and (not match) and (not is_known_third_party(obj.code_file, sdk_info=sdk_info))):
        raise app_err
    return match
