def __lt__(self, other):
    "This function helps sorted to decide how to sort.\n\n        It just checks itself against the other and decides on some key values\n        if it should be sorted higher or lower in the list.\n        The way it works:\n        For networks, every 1 in 'netmask in binary' makes the subnet more specific.\n        Therefore I chose to use prefix as the weight.\n        So a single IP (/32) should have twice the weight of a /16 network.\n        To keep everything in the same weight scale,\n        - for ipv6, we use a weight scale of 0 (all possible ipv6 addresses) to 128 (single ip)\n        - for ipv4, we use a weight scale of 0 (all possible ipv4 addresses) to 128 (single ip)\n        Therefore for ipv4, we use prefixlen (0-32) * 4 for weight,\n        which corresponds to ipv6 (0-128).\n        "
    for orderpart in self.order:
        if (orderpart == 's'):
            myweight = self.source_weight()
            hisweight = other.source_weight()
            if (myweight != hisweight):
                return (myweight > hisweight)
        elif (orderpart == 'd'):
            myweight = self.db_weight()
            hisweight = other.db_weight()
            if (myweight != hisweight):
                return (myweight < hisweight)
        elif (orderpart == 'u'):
            myweight = self.user_weight()
            hisweight = other.user_weight()
            if (myweight != hisweight):
                return (myweight < hisweight)
    try:
        return (self['src'] < other['src'])
    except TypeError:
        return (self.source_type_weight() < other.source_type_weight())
    errormessage = 'We have two rules ({1}, {2})'.format(self, other)
    errormessage += ' with exact same weight. Please file a bug.'
    raise PgHbaValueError(errormessage)