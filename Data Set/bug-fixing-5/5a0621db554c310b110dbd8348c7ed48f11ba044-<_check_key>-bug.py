def _check_key(self, key):
    if self._result.get('results', []):
        flag = False
        for res in self._result.get('results', []):
            if isinstance(res, dict):
                flag |= res.get(key, False)
        return flag
    else:
        return self._result.get(key, False)