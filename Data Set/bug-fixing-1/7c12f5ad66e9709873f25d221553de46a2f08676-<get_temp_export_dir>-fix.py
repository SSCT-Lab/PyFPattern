

def get_temp_export_dir(timestamped_export_dir):
    "Builds a directory name based on the argument but starting with 'temp-'.\n\n  This relies on the fact that TensorFlow Serving ignores subdirectories of\n  the base directory that can't be parsed as integers.\n\n  Args:\n    timestamped_export_dir: the name of the eventual export directory, e.g.\n      /foo/bar/<timestamp>\n\n  Returns:\n    A sister directory prefixed with 'temp-', e.g. /foo/bar/temp-<timestamp>.\n  "
    (dirname, basename) = os.path.split(timestamped_export_dir)
    temp_export_dir = os.path.join(compat.as_bytes(dirname), compat.as_bytes('temp-{}'.format(compat.as_str(basename))))
    return temp_export_dir
