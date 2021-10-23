def to_return(self):
    result = {
        
    }
    try:
        for returnable in self.returnables:
            result[returnable] = getattr(self, returnable)
        result = self._filter_params(result)
    except Exception:
        pass
    return result