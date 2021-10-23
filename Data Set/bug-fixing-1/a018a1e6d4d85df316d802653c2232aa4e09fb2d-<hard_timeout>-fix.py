

def hard_timeout(module, want, start):
    elapsed = (datetime.datetime.utcnow() - start)
    module.fail_json(msg=(want.msg or 'Timeout when waiting for BIG-IP'), elapsed=elapsed.seconds)
