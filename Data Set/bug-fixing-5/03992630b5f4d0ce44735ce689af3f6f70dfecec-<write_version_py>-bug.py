def write_version_py(filename='paddle/version.py'):
    cnt = "\n# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY\n#\nfull_version    = '%(major)d.%(minor)d.%(patch)s'\nmajor           = '%(major)d'\nminor           = '%(minor)d'\npatch           = '%(patch)s'\nrc              = '%(rc)d'\nistaged         = %(istaged)s\ncommit          = '%(commit)s'\nwith_mkl        = '%(with_mkl)s'\n\ndef show():\n    if istaged:\n        print('full_version:', full_version)\n        print('major:', major)\n        print('minor:', minor)\n        print('patch:', patch)\n        print('rc:', rc)\n    else:\n        print('commit:', commit)\n\ndef mkl():\n    return with_mkl\n"
    commit = git_commit()
    with open(filename, 'w') as f:
        f.write((cnt % {
            'major': get_major(),
            'minor': get_minor(),
            'patch': get_patch(),
            'rc': RC,
            'version': '${PADDLE_VERSION}',
            'commit': commit,
            'istaged': is_taged(),
            'with_mkl': '@WITH_MKL@',
        }))