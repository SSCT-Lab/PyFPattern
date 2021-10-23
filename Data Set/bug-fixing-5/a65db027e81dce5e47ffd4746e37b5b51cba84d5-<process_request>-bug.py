def process_request(self, url, datagram, method):
    '\n        Formats and Runs the API Request via Connection Plugin. Streamlined for use FROM Modules.\n\n        :param url: Connection URL to access\n        :type url: string\n        :param datagram: The prepared payload for the API Request in dictionary format\n        :type datagram: dict\n        :param method: The preferred API Request method (GET, ADD, POST, etc....)\n        :type method: basestring\n\n        :return: Dictionary containing results of the API Request via Connection Plugin\n        :rtype: dict\n        '
    data = self._tools.format_request(method, url, **datagram)
    response = self._conn.send_request(method, data)
    if HAS_FMGR_DEBUG:
        try:
            debug_dump(response, datagram, url, method)
        except BaseException:
            pass
    return response