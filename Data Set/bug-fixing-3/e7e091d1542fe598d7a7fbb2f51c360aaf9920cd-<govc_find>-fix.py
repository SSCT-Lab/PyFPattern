@app.route('/govc_find')
def govc_find():
    'Run govc find and optionally filter results'
    ofilter = (request.args.get('filter') or None)
    stdout_lines = _get_all_objs(ofilter=ofilter)
    return jsonify(stdout_lines)