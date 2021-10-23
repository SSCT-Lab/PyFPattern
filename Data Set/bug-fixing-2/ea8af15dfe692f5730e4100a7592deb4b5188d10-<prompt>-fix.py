

@staticmethod
def prompt(msg, private=False):
    prompt_string = to_bytes(msg, encoding=Display._output_encoding())
    if (sys.version_info >= (3,)):
        prompt_string = to_text(prompt_string)
    if private:
        return getpass.getpass(prompt_string)
    else:
        return input(prompt_string)
