

@mainthread
def update(self, *args):
    Builder.unload_file(join(PATH, TARGET))
    for w in Window.children[:]:
        Window.remove_widget(w)
    try:
        Window.add_widget(Builder.load_file(join(PATH, TARGET)))
    except Exception as e:
        Window.add_widget(Label(text=(e.message if getattr(e, 'message', None) else str(e))))
