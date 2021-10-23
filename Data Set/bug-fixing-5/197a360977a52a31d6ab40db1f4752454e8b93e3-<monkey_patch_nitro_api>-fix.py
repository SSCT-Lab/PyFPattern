def monkey_patch_nitro_api():
    from nssrc.com.citrix.netscaler.nitro.resource.base.Json import Json

    def new_resource_to_string_convert(self, resrc):
        dict_valid_values = dict(((k.replace('_', '', 1), v) for (k, v) in resrc.__dict__.items() if v))
        return json.dumps(dict_valid_values)
    Json.resource_to_string_convert = new_resource_to_string_convert
    from nssrc.com.citrix.netscaler.nitro.util.nitro_util import nitro_util

    @classmethod
    def object_to_string_new(cls, obj):
        output = []
        flds = obj.__dict__
        for (k, v) in ((k.replace('_', '', 1), v) for (k, v) in flds.items() if v):
            if isinstance(v, bool):
                output.append(('"%s":%s' % (k, v)))
            elif isinstance(v, (binary_type, text_type)):
                v = to_native(v, errors='surrogate_or_strict')
                output.append(('"%s":"%s"' % (k, v)))
            elif isinstance(v, int):
                output.append(('"%s":"%s"' % (k, v)))
        return ','.join(output)

    @classmethod
    def object_to_string_withoutquotes_new(cls, obj):
        output = []
        flds = obj.__dict__
        for (k, v) in ((k.replace('_', '', 1), v) for (k, v) in flds.items() if v):
            if isinstance(v, (int, bool)):
                output.append(('%s:%s' % (k, v)))
            elif isinstance(v, (binary_type, text_type)):
                v = to_native(v, errors='surrogate_or_strict')
                output.append(('%s:%s' % (k, cls.encode(v))))
        return ','.join(output)
    nitro_util.object_to_string = object_to_string_new
    nitro_util.object_to_string_withoutquotes = object_to_string_withoutquotes_new