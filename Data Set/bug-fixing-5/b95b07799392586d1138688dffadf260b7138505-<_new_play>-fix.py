def _new_play(self, play):
    return {
        'play': {
            'name': play.get_name(),
            'id': str(play._uuid),
        },
        'tasks': [],
    }