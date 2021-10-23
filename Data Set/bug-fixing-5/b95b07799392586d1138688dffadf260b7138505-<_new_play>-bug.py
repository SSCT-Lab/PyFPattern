def _new_play(self, play):
    return {
        'play': {
            'name': play.name,
            'id': str(play._uuid),
        },
        'tasks': [],
    }