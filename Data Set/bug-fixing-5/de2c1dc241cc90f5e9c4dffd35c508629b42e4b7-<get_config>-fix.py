def get_config(module, source, filter, lock=False):
    conn = get_connection(module)
    try:
        locked = False
        if lock:
            conn.lock(target=source)
            locked = True
        response = conn.get_config(source=source, filter=filter)
    except ConnectionError as e:
        module.fail_json(msg=to_text(e, errors='surrogate_then_replace').strip())
    finally:
        if locked:
            conn.unlock(target=source)
    return response