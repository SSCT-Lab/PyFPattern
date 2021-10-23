

def fetch_file(url, project=None, release=None, allow_scraping=True):
    '\n    Pull down a URL, returning a UrlResult object.\n\n    Attempts to fetch from the cache.\n    '
    if (url[(- 3):] == '...'):
        raise CannotFetchSource({
            'type': EventError.JS_MISSING_SOURCE,
            'url': expose_url(url),
        })
    if release:
        with metrics.timer('sourcemaps.release_file'):
            result = fetch_release_file(url, release)
    else:
        result = None
    cache_key = ('source:cache:v3:%s' % (md5_text(url).hexdigest(),))
    if (result is None):
        if ((not allow_scraping) or (not url.startswith(('http:', 'https:')))):
            error = {
                'type': EventError.JS_MISSING_SOURCE,
                'url': expose_url(url),
            }
            raise CannotFetchSource(error)
        logger.debug('Checking cache for url %r', url)
        result = cache.get(cache_key)
        if (result is not None):
            try:
                encoding = result[3]
            except IndexError:
                encoding = None
            result = (result[0], zlib.decompress(result[1]), result[2], encoding)
    if (result is None):
        domain = urlparse(url).netloc
        domain_key = ('source:blacklist:v2:%s' % (md5_text(domain).hexdigest(),))
        domain_result = cache.get(domain_key)
        if domain_result:
            domain_result['url'] = url
            raise CannotFetchSource(domain_result)
        headers = {
            
        }
        if (project and is_valid_origin(url, project=project)):
            token = project.get_option('sentry:token')
            if token:
                headers['X-Sentry-Token'] = token
        logger.debug('Fetching %r from the internet', url)
        with metrics.timer('sourcemaps.fetch'):
            http_session = http.build_session()
            response = None
            try:
                try:
                    start = time.time()
                    response = http_session.get(url, allow_redirects=True, verify=False, headers=headers, timeout=settings.SENTRY_SOURCE_FETCH_SOCKET_TIMEOUT, stream=True)
                    try:
                        cl = int(response.headers['content-length'])
                    except (LookupError, ValueError):
                        cl = 0
                    if (cl > settings.SENTRY_SOURCE_FETCH_MAX_SIZE):
                        raise OverflowError()
                    contents = []
                    cl = 0
                    if (response.status_code == 200):
                        for chunk in response.iter_content((16 * 1024)):
                            if ((time.time() - start) > settings.SENTRY_SOURCE_FETCH_TIMEOUT):
                                raise Timeout()
                            contents.append(chunk)
                            cl += len(chunk)
                            if (cl > settings.SENTRY_SOURCE_FETCH_MAX_SIZE):
                                raise OverflowError()
                except Exception as exc:
                    logger.debug('Unable to fetch %r', url, exc_info=True)
                    if isinstance(exc, RestrictedIPAddress):
                        error = {
                            'type': EventError.RESTRICTED_IP,
                            'url': expose_url(url),
                        }
                    elif isinstance(exc, SuspiciousOperation):
                        error = {
                            'type': EventError.SECURITY_VIOLATION,
                            'url': expose_url(url),
                        }
                    elif isinstance(exc, Timeout):
                        error = {
                            'type': EventError.JS_FETCH_TIMEOUT,
                            'url': expose_url(url),
                            'timeout': settings.SENTRY_SOURCE_FETCH_TIMEOUT,
                        }
                    elif isinstance(exc, OverflowError):
                        error = {
                            'type': EventError.JS_TOO_LARGE,
                            'url': expose_url(url),
                            'max_size': ((float(settings.SENTRY_SOURCE_FETCH_MAX_SIZE) / 1024) / 1024),
                        }
                    elif isinstance(exc, (RequestException, ZeroReturnError)):
                        error = {
                            'type': EventError.JS_GENERIC_FETCH_ERROR,
                            'value': six.text_type(type(exc)),
                            'url': expose_url(url),
                        }
                    else:
                        logger.exception(six.text_type(exc))
                        error = {
                            'type': EventError.UNKNOWN_ERROR,
                            'url': expose_url(url),
                        }
                    cache.set(domain_key, (error or ''), 300)
                    logger.warning('source.disabled', extra=error)
                    raise CannotFetchSource(error)
                body = b''.join(contents)
                z_body = zlib.compress(body)
                headers = {k.lower(): v for (k, v) in response.headers.items()}
                encoding = response.encoding
                cache.set(cache_key, (headers, z_body, response.status_code, encoding), 60)
                result = (headers, body, response.status_code, encoding)
            finally:
                if (response is not None):
                    response.close()
    if (result[2] != 200):
        logger.debug('HTTP %s when fetching %r', result[2], url, exc_info=True)
        error = {
            'type': EventError.JS_INVALID_HTTP_CODE,
            'value': result[2],
            'url': expose_url(url),
        }
        raise CannotFetchSource(error)
    if url.endswith('.js'):
        body_start = result[1][:20].lstrip()
        if (body_start[:1] == '<'):
            error = {
                'type': EventError.JS_INVALID_CONTENT,
                'url': url,
            }
            raise CannotFetchSource(error)
    if (not isinstance(result[1], six.binary_type)):
        try:
            result = (result[0], result[1].encode('utf8'), None)
        except UnicodeEncodeError:
            error = {
                'type': EventError.JS_INVALID_SOURCE_ENCODING,
                'value': 'utf8',
                'url': expose_url(url),
            }
            raise CannotFetchSource(error)
    return UrlResult(url, result[0], result[1], result[3])
