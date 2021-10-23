def response(self, result=None):
    response = self.header()
    response['result'] = result
    return response