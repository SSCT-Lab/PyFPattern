def send_request(self, **message_kwargs):
    '\n        Responsible for actual sending of data to the connection httpapi base plugin.\n        :param message_kwargs: A formatted dictionary containing request info: url, data, method\n\n        :return: Status code and response data.\n        '
    url = message_kwargs.get('url', '/')
    data = message_kwargs.get('data', '')
    method = message_kwargs.get('method', 'GET')
    try:
        (response, response_data) = self.connection.send(url, data, method=method)
        response_status = None
        if hasattr(response, 'status'):
            response_status = response.status
        else:
            response_status = response.headers.status
        return (response_status, to_text(response_data.getvalue()))
    except Exception as err:
        raise Exception(err)