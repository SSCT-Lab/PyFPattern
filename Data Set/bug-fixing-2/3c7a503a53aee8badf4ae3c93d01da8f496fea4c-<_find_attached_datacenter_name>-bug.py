

def _find_attached_datacenter_name(self, sd_name):
    '\n        Finds the name of the datacenter that a given\n        storage domain is attached to.\n\n        Args:\n            sd_name (str): Storage Domain name\n\n        Returns:\n            str: Data Center name\n\n        Raises:\n            Exception: In case storage domain in not attached to\n                an active Datacenter\n        '
    dcs_service = self._connection.system_service().data_centers_service()
    dc = search_by_attributes(dcs_service, storage=sd_name)
    if (dc is None):
        raise Exception(("Can't bring storage to state `%s`, because it seems thatit is not attached to any datacenter" % self.param('state')))
    elif (dc.status == dcstatus.UP):
        return dc.name
    else:
        raise Exception("Can't bring storage to state `%s`, because Datacenter %s is not UP")
