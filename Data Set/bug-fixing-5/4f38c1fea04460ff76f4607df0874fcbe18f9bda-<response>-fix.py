def response(self, result=None):
    response = self.header()
    if isinstance(result, binary_type):
        result = to_text(result)
    response['result'] = result
    return response