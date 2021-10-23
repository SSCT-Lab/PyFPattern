def extract_names_from_blob_uri(blob_uri, storage_suffix):
    m = re.match('^https://(?P<accountname>[^.]+)\\.blob\\.{0}/(?P<containername>[^/]+)/(?P<blobname>.+)$'.format(storage_suffix), blob_uri)
    if (not m):
        raise Exception(("unable to parse blob uri '%s'" % blob_uri))
    extracted_names = m.groupdict()
    return extracted_names