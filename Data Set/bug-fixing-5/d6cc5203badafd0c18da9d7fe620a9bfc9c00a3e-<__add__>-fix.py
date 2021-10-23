def __add__(self, other):
    '\n        + += operator\n        :param other: Other projection.\n        :type other: Projection\n        :return: self.\n        :rtype: MixedLayerType\n        '
    if (not self.finalized):
        assert (isinstance(other, Projection) or isinstance(other, Operator))
        self.inputs.append(other)
        self.parents.append(other.origin)
        return self
    else:
        raise MixedLayerType.AddToSealedMixedLayerException()