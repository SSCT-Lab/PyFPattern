def write_object_to_file(self, query_results, filename, fmt='csv', coerce_to_timestamp=False, record_time_added=False):
    "\n        Write query results to file.\n\n        Acceptable formats are:\n            - csv:\n                comma-separated-values file.  This is the default format.\n            - json:\n                JSON array.  Each element in the array is a different row.\n            - ndjson:\n                JSON array but each element is new-line deliminated\n                instead of comman deliminated like in `json`\n\n        This requires a significant amount of cleanup.\n        Pandas doesn't handle output to CSV and json in a uniform way.\n        This is especially painful for datetime types.\n        Pandas wants to write them as strings in CSV,\n        but as milisecond Unix timestamps.\n\n        By default, this function will try and leave all values as\n        they are represented in Salesforce.\n        You use the `coerce_to_timestamp` flag to force all datetimes\n        to become Unix timestamps (UTC).\n        This is can be greatly beneficial as it will make all of your\n        datetime fields look the same,\n        and makes it easier to work with in other database environments\n\n        :param query_results:       the results from a SQL query\n        :param filename:            the name of the file where the data\n                                    should be dumped to\n        :param fmt:                 the format you want the output in.\n                                    *Default:* csv.\n        :param coerce_to_timestamp: True if you want all datetime fields to be\n                                    converted into Unix timestamps.\n                                    False if you want them to be left in the\n                                    same format as they were in Salesforce.\n                                    Leaving the value as False will result\n                                    in datetimes being strings.\n                                    *Defaults to False*\n        :param record_time_added:   *(optional)* True if you want to add a\n                                    Unix timestamp field to the resulting data\n                                    that marks when the data\n                                    was fetched from Salesforce.\n                                    *Default: False*.\n        "
    fmt = fmt.lower()
    if (fmt not in ['csv', 'json', 'ndjson']):
        raise ValueError('Format value is not recognized: {0}'.format(fmt))
    df = pd.DataFrame.from_records(query_results, exclude=['attributes'])
    df.columns = [c.lower() for c in df.columns]
    if (coerce_to_timestamp and (df.shape[0] > 0)):
        object_name = query_results[0]['attributes']['type']
        self.log.info('Coercing timestamps for: %s', object_name)
        schema = self.describe_object(object_name)
        possible_timestamp_cols = [i['name'].lower() for i in schema['fields'] if ((i['type'] in ['date', 'datetime']) and (i['name'].lower() in df.columns))]
        df[possible_timestamp_cols] = df[possible_timestamp_cols].apply((lambda x: self._to_timestamp(x)))
    if record_time_added:
        fetched_time = time.time()
        df['time_fetched_from_salesforce'] = fetched_time
    if (fmt == 'csv'):
        self.log.info('Cleaning data and writing to CSV')
        possible_strings = df.columns[(df.dtypes == 'object')]
        df[possible_strings] = df[possible_strings].apply((lambda x: x.str.replace('\r\n', '')))
        df[possible_strings] = df[possible_strings].apply((lambda x: x.str.replace('\n', '')))
        df.to_csv(filename, index=False)
    elif (fmt == 'json'):
        df.to_json(filename, 'records', date_unit='s')
    elif (fmt == 'ndjson'):
        df.to_json(filename, 'records', lines=True, date_unit='s')
    return df