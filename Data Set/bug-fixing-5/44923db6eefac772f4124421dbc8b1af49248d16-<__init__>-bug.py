def __init__(self, output_layer, parameters):
    import py_paddle.swig_paddle as api
    topo = topology.Topology(output_layer)
    gm = api.GradientMachine.createFromConfigProto(topo.proto(), api.CREATE_MODE_TESTING, [api.PARAMETER_VALUE])
    for param in gm.getParameters():
        val = param.getBuf(api.PARAMETER_VALUE)
        name = param.getName()
        assert isinstance(val, api.Vector)
        val.copyFromNumpyArray(parameters.get(name).flatten())
    self.__gradient_machine__ = gm
    self.__data_types__ = topo.data_type()