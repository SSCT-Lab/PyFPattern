

def run_notebook(notebook, notebook_dir, kernel=None, no_cache=False, temp_dir='tmp_notebook'):
    "Run tutorial Jupyter notebook to catch any execution error.\n\n    Parameters\n    ----------\n    notebook : string\n        the name of the notebook to be tested\n    notebook_dir : string\n        the directory of the notebook to be tested\n    kernel : string, None\n        controls which kernel to use when running the notebook. e.g: python2\n    no_cache : '1' or False\n        controls whether to clean the temporary directory in which the\n        notebook was run and re-download any resource file. The default\n        behavior is to not clean the directory. Set to '1' to force clean the\n        directory.\n        NB: in the real CI, the tests will re-download everything since they\n        start from a clean workspace.\n    temp_dir: string\n        The temporary sub-directory directory in which to run the notebook.\n\n    Returns\n    -------\n       Returns true if the workbook runs with no warning or exception.\n    "
    logging.info("Running notebook '{}'".format(notebook))
    notebook_path = os.path.join(*([notebook_dir] + notebook.split('/')))
    working_dir = os.path.join(*([temp_dir] + notebook.split('/')))
    if (no_cache == '1'):
        logging.info("Cleaning and setting up temp directory '{}'".format(working_dir))
        shutil.rmtree(temp_dir, ignore_errors=True)
    errors = []
    notebook = None
    if (not os.path.isdir(working_dir)):
        os.makedirs(working_dir)
    try:
        notebook = nbformat.read((notebook_path + '.ipynb'), as_version=IPYTHON_VERSION)
        if (kernel is not None):
            eprocessor = ExecutePreprocessor(timeout=TIME_OUT, kernel_name=kernel)
        else:
            eprocessor = ExecutePreprocessor(timeout=TIME_OUT)
        success = False
        for i in range(ATTEMPTS):
            try:
                (nb, _) = eprocessor.preprocess(notebook, {
                    'metadata': {
                        'path': working_dir,
                    },
                })
                success = True
            except RuntimeError as rte:
                if (str(rte) != KERNEL_ERROR_MSG):
                    raise rte
                logging.info('Error starting preprocessor: {}. Attempt {}/{}'.format(str(rte), (i + 1), ATTEMPTS))
                time.sleep(1)
                continue
            break
        if (not success):
            errors.append('Error: Notebook failed to run after {} attempts.'.format(ATTEMPTS))
    except Exception as err:
        err_msg = str(err)
        errors.append(err_msg)
    finally:
        if (notebook is not None):
            output_file = os.path.join(working_dir, 'output.txt')
            nbformat.write(notebook, output_file)
            output_nb = io.open(output_file, mode='r', encoding='utf-8')
            for line in output_nb:
                if (('Warning:' in line) and ('numpy operator signatures' not in line)):
                    errors.append(('Warning:\n' + line))
        if (len(errors) > 0):
            logging.error('\n'.join(errors))
            return False
        return True
