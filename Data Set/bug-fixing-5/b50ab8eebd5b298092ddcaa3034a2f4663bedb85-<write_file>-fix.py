def write_file(module, dest, content):
    '\n    Write content to destination file dest, only if the content\n    has changed.\n    '
    changed = False
    (fd, tmpsrc) = tempfile.mkstemp(text=False)
    f = os.fdopen(fd, 'wb')
    try:
        f.write(content)
    except Exception as err:
        try:
            f.close()
        except:
            pass
        os.remove(tmpsrc)
        module.fail_json(msg=('failed to create temporary content file: %s' % to_native(err)), exception=traceback.format_exc())
    f.close()
    checksum_src = None
    checksum_dest = None
    if (not os.path.exists(tmpsrc)):
        try:
            os.remove(tmpsrc)
        except:
            pass
        module.fail_json(msg=('Source %s does not exist' % tmpsrc))
    if (not os.access(tmpsrc, os.R_OK)):
        os.remove(tmpsrc)
        module.fail_json(msg=('Source %s not readable' % tmpsrc))
    checksum_src = module.sha1(tmpsrc)
    if os.path.exists(dest):
        if (not os.access(dest, os.W_OK)):
            os.remove(tmpsrc)
            module.fail_json(msg=('Destination %s not writable' % dest))
        if (not os.access(dest, os.R_OK)):
            os.remove(tmpsrc)
            module.fail_json(msg=('Destination %s not readable' % dest))
        checksum_dest = module.sha1(dest)
    elif (not os.access(os.path.dirname(dest), os.W_OK)):
        os.remove(tmpsrc)
        module.fail_json(msg=('Destination dir %s not writable' % os.path.dirname(dest)))
    if (checksum_src != checksum_dest):
        try:
            shutil.copyfile(tmpsrc, dest)
            changed = True
        except Exception as err:
            os.remove(tmpsrc)
            module.fail_json(msg=('failed to copy %s to %s: %s' % (tmpsrc, dest, to_native(err))), exception=traceback.format_exc())
    os.remove(tmpsrc)
    return changed