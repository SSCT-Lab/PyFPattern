def setup(app):
    app.add_directive('versionextended', VersionChange)
    versionlabels['versionextended'] = 'Extended in pygame %s'
    if UPDATE_VERIONLABEL_CLASSES:
        versionlabel_classes['versionextended'] = 'extended'
    for label in ('versionadded', 'versionchanged', 'deprecated', 'versionextended'):
        app.add_config_value('{}_format'.format(label), str(versionlabels[label]), 'env')
    app.connect('config-inited', set_version_formats)