def get_aggr(self, name=None):
    '\n        Fetch details if aggregate exists.\n        :param name: Name of the aggregate to be fetched\n        :return:\n            Dictionary of current details if aggregate found\n            None if aggregate is not found\n        '
    if (name is None):
        name = self.parameters['name']
    aggr_get = self.aggr_get_iter(name)
    if (aggr_get and aggr_get.get_child_by_name('num-records') and (int(aggr_get.get_child_content('num-records')) >= 1)):
        current_aggr = dict()
        attr = aggr_get.get_child_by_name('attributes-list').get_child_by_name('aggr-attributes')
        current_aggr['service_state'] = attr.get_child_by_name('aggr-raid-attributes').get_child_content('state')
        return current_aggr
    return None