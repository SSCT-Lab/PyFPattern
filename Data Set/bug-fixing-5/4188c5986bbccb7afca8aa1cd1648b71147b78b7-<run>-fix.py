def run(self, terms, variables=None, **kwargs):
    display.vvvv(('%s' % terms))
    if isinstance(terms, list):
        return_values = []
        for term in terms:
            display.vvvv(('Term: %s' % term))
            cyberark_conn = CyberarkPassword(**term)
            return_values.append(cyberark_conn.get())
        return return_values
    else:
        cyberark_conn = CyberarkPassword(**terms)
        result = cyberark_conn.get()
        return result