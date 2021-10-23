

def request_fingerprint(request, include_headers=None):
    '\n    Return the request fingerprint.\n\n    The request fingerprint is a hash that uniquely identifies the resource the\n    request points to. For example, take the following two urls:\n\n    http://www.example.com/query?id=111&cat=222\n    http://www.example.com/query?cat=222&id=111\n\n    Even though those are two different URLs both point to the same resource\n    and are equivalent (ie. they should return the same response).\n\n    Another example are cookies used to store session ids. Suppose the\n    following page is only accessible to authenticated users:\n\n    http://www.example.com/members/offers.html\n\n    Lot of sites use a cookie to store the session id, which adds a random\n    component to the HTTP Request and thus should be ignored when calculating\n    the fingerprint.\n\n    For this reason, request headers are ignored by default when calculating\n    the fingeprint. If you want to include specific headers use the\n    include_headers argument, which is a list of Request headers to include.\n\n    '
    if include_headers:
        include_headers = tuple((to_bytes(h.lower()) for h in sorted(include_headers)))
    cache = _fingerprint_cache.setdefault(request, {
        
    })
    if (include_headers not in cache):
        fp = hashlib.sha1()
        fp.update(to_bytes(request.method))
        fp.update(to_bytes(canonicalize_url(request.url)))
        fp.update((request.body or b''))
        if include_headers:
            for hdr in include_headers:
                if (hdr in request.headers):
                    fp.update(hdr)
                    for v in request.headers.getlist(hdr):
                        fp.update(v)
        cache[include_headers] = fp.hexdigest()
    return cache[include_headers]
