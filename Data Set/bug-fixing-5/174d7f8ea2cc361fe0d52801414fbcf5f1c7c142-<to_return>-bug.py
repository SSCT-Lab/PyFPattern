def to_return(self):
    result = {
        
    }
    for returnable in self.returnables:
        result[returnable] = getattr(self, returnable)
    result = self._filter_params(result)
    return result