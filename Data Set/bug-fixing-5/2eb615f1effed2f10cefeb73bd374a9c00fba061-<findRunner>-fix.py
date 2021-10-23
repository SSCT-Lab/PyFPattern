def findRunner(self, description):
    runners = self._gitlab.runners.all(as_list=False)
    for runner in runners:
        if (runner['description'] == description):
            return self._gitlab.runners.get(runner['id'])