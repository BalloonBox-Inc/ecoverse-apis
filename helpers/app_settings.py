'''This module manages the application settings.'''


class AppSettings():
    '''Application settings.'''

    def __init__(self, d):
        for k, v in d.items():
            if isinstance(k, (list, tuple)):
                setattr(self, k, [AppSettings(x) if isinstance(x, dict) else x for x in v])
            else:
                setattr(self, k, AppSettings(v) if isinstance(v, dict) else v)
