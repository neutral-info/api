from api.v1.search import keywords


class Application(keywords.Application,):

    # design api function,
    def __init__(self):
        super(Application, self).__init__()
