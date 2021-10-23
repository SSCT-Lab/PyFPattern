def stop_volume(name):
    run_gluster_yes(['volume', 'stop', name])