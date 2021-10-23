

def provider(input_types=None, should_shuffle=None, pool_size=(- 1), min_pool_size=(- 1), can_over_batch_size=True, calc_batch_size=None, cache=CacheType.NO_CACHE, check=False, check_fail_continue=False, init_hook=None, **kwargs):
    "\n    Provider decorator. Use it to make a function into PyDataProvider2 object.\n    In this function, user only need to get each sample for some train/test\n    file.\n\n    The basic usage is:\n\n    ..  code-block:: python\n\n        @provider(some data provider config here...)\n        def process(settings, file_name):\n            while not at end of file_name:\n                sample = readOneSampleFromFile(file_name)\n                yield sample.\n\n    The configuration of data provider should be setup by\\:\n\n    :param input_types: Specify the input types, can also be set in init_hook.\n                        It could be a list of InputType object. For example,\n                        input_types=[dense_vector(9), integer_value(2)]. Or user\n                        can set a dict of InputType object, which key is\n                        data_layer's name. For example, input_types=                        {'img': img_features, 'label': label}. when using dict of\n                        InputType, user could yield a dict of feature values, which\n                        key is also data_layer's name.\n\n    :type input_types: list|tuple|dict\n\n    :param should_shuffle: True if data should shuffle. Pass None means shuffle\n                           when is training and not to shuffle when is testing.\n    :type should_shuffle: bool\n\n    :param pool_size: Max number of sample in data pool.\n    :type pool_size: int\n\n    :param min_pool_size: Set minimal sample in data pool. The PaddlePaddle will\n                          random pick sample in pool. So the min_pool_size\n                          effect the randomize of data.\n    :type min_pool_size: int\n\n    :param can_over_batch_size: True if paddle can return a mini-batch larger\n                                than batch size in settings. It is useful when\n                                custom calculate one sample's batch_size.\n\n                                It is very danger to set it to false and use\n                                calc_batch_size together. Default is false.\n    :type can_over_batch_size: bool\n\n    :param calc_batch_size: a method to calculate each sample's batch size.\n                            Default each sample's batch size is 1. But to you\n                            can customize each sample's batch size.\n    :type calc_batch_size: callable\n\n    :param cache: Cache strategy of Data Provider. Default is CacheType.NO_CACHE\n    :type cache: int\n\n    :param init_hook: Initialize hook. Useful when data provider need load some\n                      external data like dictionary. The parameter is\n                      (settings, file_list, \\*\\*kwargs).\n\n                      - settings. It is the global settings object. User can set\n                        settings.input_types here.\n                      - file_list. All file names for passed to data provider.\n                      - is_train. Is this data provider used for training or not.\n                      - kwargs. Other keyword arguments passed from\n                        trainer_config's args parameter.\n    :type init_hook: callable\n\n    :param check: Check the yield data format is as same as input_types. Enable\n                  this will make data provide process slow but it is very useful\n                  for debug. Default is disabled.\n    :type check: bool\n\n    :param check_fail_continue: Continue train or not when check failed. Just\n                                drop the wrong format data when it is True. Has\n                                no effect when check set to False.\n    :type check_fail_continue: bool\n    "

    def __wrapper__(generator):

        class DataProvider(object):

            def __init__(self, file_list, **kwargs):
                self.logger = logging.getLogger('')
                self.logger.setLevel(logging.INFO)
                self.input_types = None
                if ('slots' in kwargs):
                    self.logger.warning('setting slots value is deprecated, please use input_types instead.')
                    self.slots = kwargs['slots']
                self.slots = input_types
                self.should_shuffle = should_shuffle
                true_table = [1, 't', 'true', 'on']
                false_table = [0, 'f', 'false', 'off']
                if ((not isinstance(self.should_shuffle, bool)) and (self.should_shuffle is not None)):
                    if isinstance(self.should_shuffle, basestring):
                        self.should_shuffle = self.should_shuffle.lower()
                    if (self.should_shuffle in true_table):
                        self.should_shuffle = True
                    elif (self.should_shuffle in false_table):
                        self.should_shuffle = False
                    else:
                        self.logger.warning(('Could not recognize should_shuffle (%s), just use default value of should_shuffle. Please set should_shuffle to bool value or something in %s' % (repr(self.should_shuffle), repr((true_table + false_table)))))
                        self.should_shuffle = None
                self.pool_size = pool_size
                self.can_over_batch_size = can_over_batch_size
                self.calc_batch_size = calc_batch_size
                self.file_list = file_list
                self.generator = generator
                self.cache = cache
                self.min_pool_size = min_pool_size
                self.input_order = kwargs['input_order']
                self.check = check
                if (init_hook is not None):
                    init_hook(self, file_list=file_list, **kwargs)
                if (self.input_types is not None):
                    self.slots = self.input_types
                assert (self.slots is not None)
                assert (self.generator is not None)
                use_dynamic_order = False
                if isinstance(self.slots, dict):
                    self.slots = [self.slots[ipt] for ipt in self.input_order]
                    use_dynamic_order = True
                if (len(self.slots) == 1):
                    self.generator = SingleSlotWrapper(self.generator)
                if use_dynamic_order:
                    self.generator = InputOrderWrapper(self.generator, self.input_order)
                else:
                    self.generator = CheckInputTypeWrapper(self.generator, self.slots, self.logger)
                if self.check:
                    self.generator = CheckWrapper(self.generator, self.slots, check_fail_continue, self.logger)
        return DataProvider
    return __wrapper__
