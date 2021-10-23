def download(self, url):
    '\n        Download the given URL and return the file name.\n        '

    def cleanup_url(url):
        tmp = url.rstrip('/')
        filename = tmp.split('/')[(- 1)]
        if url.endswith('/'):
            display_url = (tmp + '/')
        else:
            display_url = url
        return (filename, display_url)
    prefix = ('django_%s_template_' % self.app_or_project)
    tempdir = tempfile.mkdtemp(prefix=prefix, suffix='_download')
    self.paths_to_remove.append(tempdir)
    (filename, display_url) = cleanup_url(url)
    if (self.verbosity >= 2):
        self.stdout.write(('Downloading %s\n' % display_url))
    try:
        (the_path, info) = urlretrieve(url, path.join(tempdir, filename))
    except OSError as e:
        raise CommandError(("couldn't download URL %s to %s: %s" % (url, filename, e)))
    used_name = the_path.split('/')[(- 1)]
    content_disposition = info.get('content-disposition')
    if content_disposition:
        (_, params) = cgi.parse_header(content_disposition)
        guessed_filename = (params.get('filename') or used_name)
    else:
        guessed_filename = used_name
    ext = self.splitext(guessed_filename)[1]
    content_type = info.get('content-type')
    if ((not ext) and content_type):
        ext = mimetypes.guess_extension(content_type)
        if ext:
            guessed_filename += ext
    if (used_name != guessed_filename):
        guessed_path = path.join(tempdir, guessed_filename)
        shutil.move(the_path, guessed_path)
        return guessed_path
    return the_path