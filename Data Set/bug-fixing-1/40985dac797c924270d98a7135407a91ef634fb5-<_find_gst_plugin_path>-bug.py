

def _find_gst_plugin_path():
    'Returns a list of directories to search for GStreamer plugins.\n    '
    if ('GST_PLUGIN_PATH' in environ):
        return [os.path.abspath(os.path.expanduser(path)) for path in environ['GST_PLUGIN_PATH'].split(os.pathsep)]
    try:
        p = subprocess.Popen(['gst-inspect-1.0', 'coreelements'], stdout=subprocess.PIPE)
    except:
        return []
    (stdoutdata, stderrdata) = p.communicate()
    match = re.search(b'\\s+(\\S+libgstcoreelements\\.\\S+)', stdoutdata)
    if (not match):
        return []
    return [os.path.dirname(match.group(1))]
