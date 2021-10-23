@app.route('/govc_find')
def govc_find():
    'Run govc find and optionally filter results'
    global GOVCURL
    ofilter = (request.args.get('filter') or None)
    env = {
        'GOPATH': GOPATH,
        'GOVC_URL': GOVCURL,
        'GOVC_INSECURE': '1',
    }
    cmd = ('%s find 2>&1' % GOVCPATH)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, shell=True)
    (so, se) = p.communicate()
    stdout_lines = so.split('\n')
    if ofilter:
        stdout_lines = [x for x in stdout_lines if (ofilter in x)]
    return jsonify(stdout_lines)