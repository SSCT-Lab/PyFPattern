

def root_app(env, resp):
    resp(b'404 Not Found', [('Content-Type', 'text/plain')])
    return [b'Apache Airflow is not at this location']
