@classmethod
def from_custom_template(cls, searchpath, name):
    '\n        Factory function for creating a subclass of ``Styler``\n        with a custom template and Jinja environment.\n\n        Parameters\n        ----------\n        searchpath : str or list\n            Path or paths of directories containing the templates.\n        name : str\n            Name of your custom template to use for rendering.\n\n        Returns\n        -------\n        MyStyler : subclass of Styler\n            Has the correct ``env`` and ``template`` class attributes set.\n        '
    loader = jinja2.ChoiceLoader([jinja2.FileSystemLoader(searchpath), cls.loader])

    class MyStyler(cls):
        env = jinja2.Environment(loader=loader)
        template = env.get_template(name)
    return MyStyler