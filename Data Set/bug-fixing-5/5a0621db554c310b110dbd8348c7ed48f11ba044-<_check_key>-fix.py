def _check_key(self, key):
    "get a specific key from the result or it's items"
    if (isinstance(self._result, dict) and (key in self._result)):
        return self._result.get(key, False)
    else:
        flag = False
        for res in self._result.get('results', []):
            if isinstance(res, dict):
                flag |= res.get(key, False)
        return flag