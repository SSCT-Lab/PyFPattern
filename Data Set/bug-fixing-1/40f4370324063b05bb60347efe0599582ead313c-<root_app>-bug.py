

def root_app(env, resp):
    resp(b'404 Not Found', [(b'Content-Type', b'text/plain')])
    return [b'Apache Airflow is not at this location']
