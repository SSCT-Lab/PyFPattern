

def _load_handlers(self, attr, ds):
    '\n        Loads a list of blocks from a list which may be mixed handlers/blocks.\n        Bare handlers outside of a block are given an implicit block.\n        '
    try:
        return load_list_of_blocks(ds=ds, play=self, use_handlers=True, variable_manager=self._variable_manager, loader=self._loader)
    except AssertionError as e:
        raise AnsibleParserError('A malformed block was encountered while loading handlers', obj=self._ds, orig_exc=e)
