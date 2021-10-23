def get_conn(self):
    '\n        Fetches PyMongo Client\n        '
    if (self.client is not None):
        return self.client
    conn = self.connection
    uri = 'mongodb://{creds}{host}{port}/{database}'.format(creds=('{}:{}@'.format(conn.login, conn.password) if (conn.login is not None) else ''), host=conn.host, port=('' if (conn.port is None) else ':{}'.format(conn.port)), database=('' if (conn.schema is None) else conn.schema))
    options = self.extras
    if options.get('ssl', False):
        options.update({
            'ssl_cert_reqs': CERT_NONE,
        })
    self.client = MongoClient(uri, **options)
    return self.client