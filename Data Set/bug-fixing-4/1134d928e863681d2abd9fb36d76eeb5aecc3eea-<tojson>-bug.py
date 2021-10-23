def tojson(self):
    'Save symbol into a JSON string.\n\n        See Also\n        --------\n        symbol.load_json : Used to load symbol from JSON string.\n        '
    json_str = ctypes.c_char_p()
    check_call(_LIB.MXSymbolSaveToJSON(self.handle, ctypes.byref(json_str)))
    return py_str(json_str.value)