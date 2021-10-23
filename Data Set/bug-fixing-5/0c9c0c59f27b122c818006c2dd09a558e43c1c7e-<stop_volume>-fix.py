def stop_volume(name):
    run_gluster(['volume', 'stop', name])