def get_value(self, result):
    if (self.encoding in ['json', 'text']):
        try:
            return self.get_json(result)
        except (IndexError, TypeError, AttributeError):
            msg = 'unable to apply conditional to result'
            raise FailedConditionalError(msg, self.raw)
    elif (self.encoding == 'xml'):
        return self.get_xml(result.get('result'))