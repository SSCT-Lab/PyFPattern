def fetch_lfw_people(data_home=None, funneled=True, resize=0.5, min_faces_per_person=0, color=False, slice_=(slice(70, 195), slice(78, 172)), download_if_missing=True):
    "Loader for the Labeled Faces in the Wild (LFW) people dataset\n\n    This dataset is a collection of JPEG pictures of famous people\n    collected on the internet, all details are available on the\n    official website:\n\n        http://vis-www.cs.umass.edu/lfw/\n\n    Each picture is centered on a single face. Each pixel of each channel\n    (color in RGB) is encoded by a float in range 0.0 - 1.0.\n\n    The task is called Face Recognition (or Identification): given the\n    picture of a face, find the name of the person given a training set\n    (gallery).\n\n    The original images are 250 x 250 pixels, but the default slice and resize\n    arguments reduce them to 62 x 47.\n\n    Parameters\n    ----------\n    data_home : optional, default: None\n        Specify another download and cache folder for the datasets. By default\n        all scikit learn data is stored in '~/scikit_learn_data' subfolders.\n\n    funneled : boolean, optional, default: True\n        Download and use the funneled variant of the dataset.\n\n    resize : float, optional, default 0.5\n        Ratio used to resize the each face picture.\n\n    min_faces_per_person : int, optional, default None\n        The extracted dataset will only retain pictures of people that have at\n        least `min_faces_per_person` different pictures.\n\n    color : boolean, optional, default False\n        Keep the 3 RGB channels instead of averaging them to a single\n        gray level channel. If color is True the shape of the data has\n        one more dimension than the shape with color = False.\n\n    slice_ : optional\n        Provide a custom 2D slice (height, width) to extract the\n        'interesting' part of the jpeg files and avoid use statistical\n        correlation from the background\n\n    download_if_missing : optional, True by default\n        If False, raise a IOError if the data is not locally available\n        instead of trying to download the data from the source site.\n\n    Returns\n    -------\n    dataset : dict-like object with the following attributes:\n\n    dataset.data : numpy array of shape (13233, 2914)\n        Each row corresponds to a ravelled face image of original size 62 x 47\n        pixels. Changing the ``slice_`` or resize parameters will change the\n        shape of the output.\n\n    dataset.images : numpy array of shape (13233, 62, 47)\n        Each row is a face image corresponding to one of the 5749 people in\n        the dataset. Changing the ``slice_`` or resize parameters will change\n        the shape of the output.\n\n    dataset.target : numpy array of shape (13233,)\n        Labels associated to each face image. Those labels range from 0-5748\n        and correspond to the person IDs.\n\n    dataset.DESCR : string\n        Description of the Labeled Faces in the Wild (LFW) dataset.\n    "
    (lfw_home, data_folder_path) = check_fetch_lfw(data_home=data_home, funneled=funneled, download_if_missing=download_if_missing)
    logger.info('Loading LFW people faces from %s', lfw_home)
    m = Memory(cachedir=lfw_home, compress=6, verbose=0)
    load_func = m.cache(_fetch_lfw_people)
    (faces, target, target_names) = load_func(data_folder_path, resize=resize, min_faces_per_person=min_faces_per_person, color=color, slice_=slice_)
    return Bunch(data=faces.reshape(len(faces), (- 1)), images=faces, target=target, target_names=target_names, DESCR='LFW faces dataset')