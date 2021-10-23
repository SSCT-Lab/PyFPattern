

def _update_from(self, obj):
    '\n        Copies some attributes of obj to self.\n\n        '
    if ((obj is not None) and isinstance(obj, ndarray)):
        _baseclass = type(obj)
    else:
        _baseclass = ndarray
    _optinfo = {
        
    }
    _optinfo.update(getattr(obj, '_optinfo', {
        
    }))
    _optinfo.update(getattr(obj, '_basedict', {
        
    }))
    if (not isinstance(obj, MaskedArray)):
        _optinfo.update(getattr(obj, '__dict__', {
            
        }))
    _dict = dict(_fill_value=getattr(obj, '_fill_value', None), _hardmask=getattr(obj, '_hardmask', False), _sharedmask=getattr(obj, '_sharedmask', False), _isfield=getattr(obj, '_isfield', False), _baseclass=getattr(obj, '_baseclass', _baseclass), _optinfo=_optinfo, _basedict=_optinfo)
    self.__dict__.update(_dict)
    self.__dict__.update(_optinfo)
    return
