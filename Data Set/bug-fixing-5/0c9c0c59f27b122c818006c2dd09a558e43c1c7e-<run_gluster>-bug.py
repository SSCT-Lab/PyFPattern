def run_gluster(gargs, **kwargs):
    global glusterbin
    global module
    args = [glusterbin]
    args.extend(gargs)
    try:
        (rc, out, err) = module.run_command(args, **kwargs)
        if (rc != 0):
            module.fail_json(msg=('error running gluster (%s) command (rc=%d): %s' % (' '.join(args), rc, (out or err))), exception=traceback.format_exc())
    except Exception as e:
        module.fail_json(msg=('error running gluster (%s) command: %s' % (' '.join(args), to_native(e))), exception=traceback.format_exc())
    return out