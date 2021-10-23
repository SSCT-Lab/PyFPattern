def local_envra(path):
    'return envra of a local rpm passed in'
    ts = rpm.TransactionSet()
    ts.setVSFlags(rpm._RPMVSF_NOSIGNATURES)
    fd = os.open(path, os.O_RDONLY)
    try:
        header = ts.hdrFromFdno(fd)
    finally:
        os.close(fd)
    return ('%s:%s-%s-%s.%s' % ((header[rpm.RPMTAG_EPOCH] or '0'), header[rpm.RPMTAG_NAME], header[rpm.RPMTAG_VERSION], header[rpm.RPMTAG_RELEASE], header[rpm.RPMTAG_ARCH]))