def restrict_to_hosts(self, restriction):
    " \n        Restrict list operations to the hosts given in restriction.  This is used\n        to batch serial operations in main playbook code, don't use this for other\n        reasons.\n        "
    if (restriction is None):
        return
    elif (not isinstance(restriction, list)):
        restriction = [restriction]
    self._restriction = [h.name for h in restriction]