def disconnect(self, cid):
    '\n        disconnect the callback registered with callback id *cid*\n        '
    for (eventname, callbackd) in list(six.iteritems(self.callbacks)):
        try:
            del callbackd[cid]
        except KeyError:
            continue
        else:
            for (signal, functions) in list(six.iteritems(self._func_cid_map)):
                for (function, value) in list(six.iteritems(functions)):
                    if (value == cid):
                        del functions[function]
            return