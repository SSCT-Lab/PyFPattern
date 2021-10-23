def dropna(self, axis=0, how='any', thresh=None, subset=None, inplace=False):
    '\n        Remove missing values.\n\n        See the :ref:`User Guide <missing_data>` for more on which values are\n        considered missing, and how to work with missing data.\n\n        Parameters\n        ----------\n        axis : {0 or \'index\', 1 or \'columns\'}, default 0\n            Determine if rows or columns which contain missing values are\n            removed.\n\n            * 0, or \'index\' : Drop rows which contain missing values.\n            * 1, or \'columns\' : Drop columns which contain missing value.\n\n            .. deprecated:: 0.23.0\n                Pass tuple or list to drop on multiple axes.\n\n        how : {\'any\', \'all\'}, default \'any\'\n            Determine if row or column is removed from DataFrame, when we have\n            at least one NA or all NA.\n\n            * \'any\' : If any NA values are present, drop that row or column.\n            * \'all\' : If all values are NA, drop that row or column.\n        thresh : int, optional\n            Require that many non-NA values.\n        subset : array-like, optional\n            Labels along other axis to consider, e.g. if you are dropping rows\n            these would be a list of columns to include.\n        inplace : bool, default False\n            If True, do operation inplace and return None.\n\n        Returns\n        -------\n        DataFrame\n            DataFrame with NA entries dropped from it.\n\n        See Also\n        --------\n        DataFrame.isna: Indicate missing values.\n        DataFrame.notna : Indicate existing (non-missing) values.\n        DataFrame.fillna : Replace missing values.\n        Series.dropna : Drop missing values.\n        Index.dropna : Drop missing indices.\n\n        Examples\n        --------\n        >>> df = pd.DataFrame({"name": [\'Alfred\', \'Batman\', \'Catwoman\'],\n        ...                    "toy": [np.nan, \'Batmobile\', \'Bullwhip\'],\n        ...                    "born": [pd.NaT, pd.Timestamp("1940-04-25"),\n        ...                             pd.NaT]})\n        >>> df\n               name        toy       born\n        0    Alfred        NaN        NaT\n        1    Batman  Batmobile 1940-04-25\n        2  Catwoman   Bullwhip        NaT\n\n        Drop the rows where at least one element is missing.\n\n        >>> df.dropna()\n             name        toy       born\n        1  Batman  Batmobile 1940-04-25\n\n        Drop the columns where at least one element is missing.\n\n        >>> df.dropna(axis=\'columns\')\n               name\n        0    Alfred\n        1    Batman\n        2  Catwoman\n\n        Drop the rows where all elements are missing.\n\n        >>> df.dropna(how=\'all\')\n               name        toy       born\n        0    Alfred        NaN        NaT\n        1    Batman  Batmobile 1940-04-25\n        2  Catwoman   Bullwhip        NaT\n\n        Keep only the rows with at least 2 non-NA values.\n\n        >>> df.dropna(thresh=2)\n               name        toy       born\n        1    Batman  Batmobile 1940-04-25\n        2  Catwoman   Bullwhip        NaT\n\n        Define in which columns to look for missing values.\n\n        >>> df.dropna(subset=[\'name\', \'born\'])\n               name        toy       born\n        1    Batman  Batmobile 1940-04-25\n\n        Keep the DataFrame with valid entries in the same variable.\n\n        >>> df.dropna(inplace=True)\n        >>> df\n             name        toy       born\n        1  Batman  Batmobile 1940-04-25\n        '
    inplace = validate_bool_kwarg(inplace, 'inplace')
    if isinstance(axis, (tuple, list)):
        msg = 'supplying multiple axes to axis is deprecated and will be removed in a future version.'
        warnings.warn(msg, FutureWarning, stacklevel=2)
        result = self
        for ax in axis:
            result = result.dropna(how=how, thresh=thresh, subset=subset, axis=ax)
    else:
        axis = self._get_axis_number(axis)
        agg_axis = (1 - axis)
        agg_obj = self
        if (subset is not None):
            ax = self._get_axis(agg_axis)
            indices = ax.get_indexer_for(subset)
            check = (indices == (- 1))
            if check.any():
                raise KeyError(list(np.compress(check, subset)))
            agg_obj = self.take(indices, axis=agg_axis)
        count = agg_obj.count(axis=agg_axis)
        if (thresh is not None):
            mask = (count >= thresh)
        elif (how == 'any'):
            mask = (count == len(agg_obj._get_axis(agg_axis)))
        elif (how == 'all'):
            mask = (count > 0)
        elif (how is not None):
            raise ValueError('invalid how option: {h}'.format(h=how))
        else:
            raise TypeError('must specify how or thresh')
        result = self._take(mask.nonzero()[0], axis=axis)
    if inplace:
        self._update_inplace(result)
    else:
        return result