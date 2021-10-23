def to_xarray(self):
    "\n        Return an xarray object from the pandas object.\n\n        Returns\n        -------\n        xarray.DataArray or xarray.Dataset\n            Data in the pandas structure converted to Dataset if the object is\n            a DataFrame, or a DataArray if the object is a Series.\n\n        See Also\n        --------\n        DataFrame.to_hdf : Write DataFrame to an HDF5 file.\n        DataFrame.to_parquet : Write a DataFrame to the binary parquet format.\n\n        Notes\n        -----\n        See the `xarray docs <http://xarray.pydata.org/en/stable/>`__\n\n        Examples\n        --------\n        >>> df = pd.DataFrame([('falcon', 'bird', 389.0, 2),\n        ...                    ('parrot', 'bird', 24.0, 2),\n        ...                    ('lion', 'mammal', 80.5, 4),\n        ...                    ('monkey', 'mammal', np.nan, 4)],\n        ...                   columns=['name', 'class', 'max_speed',\n        ...                            'num_legs'])\n        >>> df\n             name   class  max_speed  num_legs\n        0  falcon    bird      389.0         2\n        1  parrot    bird       24.0         2\n        2    lion  mammal       80.5         4\n        3  monkey  mammal        NaN         4\n\n        >>> df.to_xarray()\n        <xarray.Dataset>\n        Dimensions:    (index: 4)\n        Coordinates:\n          * index      (index) int64 0 1 2 3\n        Data variables:\n            name       (index) object 'falcon' 'parrot' 'lion' 'monkey'\n            class      (index) object 'bird' 'bird' 'mammal' 'mammal'\n            max_speed  (index) float64 389.0 24.0 80.5 nan\n            num_legs   (index) int64 2 2 4 4\n\n        >>> df['max_speed'].to_xarray()\n        <xarray.DataArray 'max_speed' (index: 4)>\n        array([389. ,  24. ,  80.5,   nan])\n        Coordinates:\n          * index    (index) int64 0 1 2 3\n\n        >>> dates = pd.to_datetime(['2018-01-01', '2018-01-01',\n        ...                         '2018-01-02', '2018-01-02'])\n        >>> df_multiindex = pd.DataFrame({'date': dates,\n        ...                               'animal': ['falcon', 'parrot',\n        ...                                          'falcon', 'parrot'],\n        ...                               'speed': [350, 18, 361, 15]})\n        >>> df_multiindex = df_multiindex.set_index(['date', 'animal'])\n\n        >>> df_multiindex\n                           speed\n        date       animal\n        2018-01-01 falcon    350\n                   parrot     18\n        2018-01-02 falcon    361\n                   parrot     15\n\n        >>> df_multiindex.to_xarray()\n        <xarray.Dataset>\n        Dimensions:  (animal: 2, date: 2)\n        Coordinates:\n          * date     (date) datetime64[ns] 2018-01-01 2018-01-02\n          * animal   (animal) object 'falcon' 'parrot'\n        Data variables:\n            speed    (date, animal) int64 350 18 361 15\n        "
    xarray = import_optional_dependency('xarray')
    if (self.ndim == 1):
        return xarray.DataArray.from_series(self)
    else:
        return xarray.Dataset.from_dataframe(self)