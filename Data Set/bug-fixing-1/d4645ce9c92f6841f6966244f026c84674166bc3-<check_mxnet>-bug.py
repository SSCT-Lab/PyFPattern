

def check_mxnet():
    print('----------MXNet Info-----------')
    try:
        import mxnet
        print('Version      :', mxnet.__version__)
        mx_dir = os.path.dirname(mxnet.__file__)
        print('Directory    :', mx_dir)
        commit_hash = os.path.join(mx_dir, 'COMMIT_HASH')
        with open(commit_hash, 'r') as f:
            ch = f.read().strip()
            print('Commit Hash   :', ch)
    except ImportError:
        print('No MXNet installed.')
    except FileNotFoundError:
        print('Hashtag not found. Not installed from pre-built package.')
    except Exception as e:
        import traceback
        if (not isinstance(e, IOError)):
            print('An error occured trying to import mxnet.')
            print('This is very likely due to missing missing or incompatible library files.')
        print(traceback.format_exc())
