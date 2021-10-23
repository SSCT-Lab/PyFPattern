

def getMatchingRecord(self, record_name, record_type, record_value):
    if (not self.all_records):
        self.all_records = self.getRecords()
    if (record_type in ['A', 'AAAA', 'CNAME', 'ANAME', 'HTTPRED', 'PTR']):
        for result in self.all_records:
            if ((result['name'] == record_name) and (result['type'] == record_type)):
                return result
        return False
    elif (record_type in ['MX', 'NS', 'TXT', 'SRV']):
        for result in self.all_records:
            if (record_type == 'MX'):
                value = record_value.split(' ')[1]
            elif (record_type == 'SRV'):
                value = record_value.split(' ')[3]
            else:
                value = record_value
            if ((result['name'] == record_name) and (result['type'] == record_type) and (result['value'] == value)):
                return result
        return False
    else:
        raise Exception('record_type not yet supported')
