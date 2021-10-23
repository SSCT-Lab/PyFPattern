def monkey_patch_nitro_api():
    from nssrc.com.citrix.netscaler.nitro.resource.base.Json import Json

    def new_resource_to_string_convert(self, resrc):
        try:
            dict_valid_values = dict(((k.replace('_', '', 1), v) for (k, v) in resrc.__dict__.items() if v))
            return json.dumps(dict_valid_values)
        except Exception as e:
            raise e
    Json.resource_to_string_convert = new_resource_to_string_convert
    from nssrc.com.citrix.netscaler.nitro.util.nitro_util import nitro_util

    @classmethod
    def object_to_string_new(cls, obj):
        try:
            str_ = ''
            flds = obj.__dict__
            flds = dict(((k.replace('_', '', 1), v) for (k, v) in flds.items() if v))
            if flds:
                for (k, v) in flds.items():
                    str_ = (((str_ + '"') + k) + '":')
                    if (type(v) is unicode):
                        v = v.encode('utf8')
                    if (type(v) is bool):
                        str_ = (str_ + v)
                    elif (type(v) is str):
                        str_ = (((str_ + '"') + v) + '"')
                    elif (type(v) is int):
                        str_ = (((str_ + '"') + str(v)) + '"')
                    if str_:
                        str_ = (str_ + ',')
            return str_
        except Exception as e:
            raise e

    @classmethod
    def object_to_string_withoutquotes_new(cls, obj):
        try:
            str_ = ''
            flds = obj.__dict__
            flds = dict(((k.replace('_', '', 1), v) for (k, v) in flds.items() if v))
            i = 0
            if flds:
                for (k, v) in flds.items():
                    str_ = ((str_ + k) + ':')
                    if (type(v) is unicode):
                        v = v.encode('utf8')
                    if (type(v) is bool):
                        str_ = (str_ + v)
                    elif (type(v) is str):
                        str_ = (str_ + cls.encode(v))
                    elif (type(v) is int):
                        str_ = (str_ + str(v))
                    i = (i + 1)
                    if ((i != len(flds.items())) and str_):
                        str_ = (str_ + ',')
            return str_
        except Exception as e:
            raise e
    nitro_util.object_to_string = object_to_string_new
    nitro_util.object_to_string_withoutquotes = object_to_string_withoutquotes_new