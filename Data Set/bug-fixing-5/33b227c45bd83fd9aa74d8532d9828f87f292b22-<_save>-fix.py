def _save(obj, f, pickle_module, pickle_protocol):
    import torch.nn as nn
    serialized_tensors = {
        
    }
    serialized_storages = {
        
    }
    serialized_container_types = {
        
    }

    def persistent_id(obj):
        if (isinstance(obj, type) and issubclass(obj, nn.Container)):
            if (obj in serialized_container_types):
                return None
            serialized_container_types[obj] = True
            source_file = source = None
            try:
                source_file = inspect.getsourcefile(obj)
                source = inspect.getsource(obj)
            except (TypeError, IOError):
                warnings.warn((("Couldn't retrieve source code for container of type " + obj.__name__) + ". It won't be checked for correctness upon loading."))
            return (obj, source_file, source)
        if torch.is_tensor(obj):
            serialized_tensors[obj._cdata] = obj
            return str(obj._cdata)
        elif torch.is_storage(obj):
            serialized_storages[obj._cdata] = obj
            return str(obj._cdata)
        return None

    def save_tensors(f):
        pickle_module.dump(len(serialized_tensors), f, protocol=pickle_protocol)
        for (key, tensor) in serialized_tensors.items():
            storage = tensor.storage()
            if (storage is not None):
                storage_id = storage._cdata
                serialized_storages[storage_id] = storage
            else:
                storage_id = None
            pickle_module.dump((key, storage_id, type(tensor)), f, protocol=pickle_protocol)
            f.flush()
            tensor._write_metadata(f)

    def save_storages(f):
        storage_views = []
        storage_views_roots = {
            
        }
        for (key, storage) in serialized_storages.items():
            (root, offset) = storage._root_storage()
            if (root is not storage):
                storage_views_roots[root._cdata] = root
                storage_views.append((storage._cdata, root._cdata, offset, storage.size()))
        for view_info in storage_views:
            del serialized_storages[view_info[0]]
        serialized_storages.update(storage_views_roots)
        pickle_module.dump(len(serialized_storages), f, protocol=pickle_protocol)
        for (key, storage) in serialized_storages.items():
            location = location_tag(storage)
            storage_type = normalize_storage_type(type(storage))
            pickle_module.dump((key, location, storage_type), f, protocol=pickle_protocol)
            f.flush()
            storage._write_file(f)
        pickle_module.dump(storage_views, f, protocol=pickle_protocol)

    def pickle_objects(f):
        pickler = pickle_module.Pickler(f, protocol=pickle_protocol)
        pickler.persistent_id = persistent_id
        pickler.dump(obj)

    def save_sys_info(f):
        sys_info = dict(protocol_version=1000, little_endian=(sys.byteorder == 'little'), type_sizes=dict(short=SHORT_SIZE, int=INT_SIZE, long=LONG_SIZE))
        pickle_module.dump(sys_info, f, protocol=pickle_protocol)
    with closing(tarfile.open(fileobj=f, mode='w:', format=tarfile.PAX_FORMAT)) as tar:
        _add_to_tar(save_sys_info, tar, 'sys_info')
        _add_to_tar(pickle_objects, tar, 'pickle')
        _add_to_tar(save_tensors, tar, 'tensors')
        _add_to_tar(save_storages, tar, 'storages')