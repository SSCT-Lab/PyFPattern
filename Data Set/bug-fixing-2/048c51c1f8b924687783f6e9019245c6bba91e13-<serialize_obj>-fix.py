

def serialize_obj(self, obj, class_name, enum_modules=None):
    "\n        Return a JSON representation of an Azure object.\n\n        :param obj: Azure object\n        :param class_name: Name of the object's class\n        :param enum_modules: List of module names to build enum dependencies from.\n        :return: serialized result\n        "
    enum_modules = ([] if (enum_modules is None) else enum_modules)
    dependencies = dict()
    if enum_modules:
        for module_name in enum_modules:
            mod = importlib.import_module(module_name)
            for (mod_class_name, mod_class_obj) in inspect.getmembers(mod, predicate=inspect.isclass):
                dependencies[mod_class_name] = mod_class_obj
        self.log('dependencies: ')
        self.log(str(dependencies))
    serializer = Serializer(classes=dependencies)
    return serializer.body(obj, class_name, keep_readonly=True)
