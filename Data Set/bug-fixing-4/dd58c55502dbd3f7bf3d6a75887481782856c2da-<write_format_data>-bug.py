def write_format_data(self, format_dict, md_dict=None):
    'Write the format data dict to the frontend.\n\n        This default version of this method simply writes the plain text\n        representation of the object to ``sys.stdout``. Subclasses should\n        override this method to send the entire `format_dict` to the\n        frontends.\n\n        Parameters\n        ----------\n        format_dict : dict\n            The format dict for the object passed to `sys.displayhook`.\n        md_dict : dict (optional)\n            The metadata dict to be associated with the display data.\n        '
    if ('text/plain' not in format_dict):
        return
    result_repr = format_dict['text/plain']
    if ('\n' in result_repr):
        if (not self.prompt_end_newline):
            result_repr = ('\n' + result_repr)
    print(result_repr)