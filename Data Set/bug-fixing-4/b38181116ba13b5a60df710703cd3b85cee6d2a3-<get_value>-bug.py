def get_value(self, result):
    if (self.encoding in ['json', 'text']):
        return self.get_json(result)
    elif (self.encoding == 'xml'):
        return self.get_xml(result.get('result'))