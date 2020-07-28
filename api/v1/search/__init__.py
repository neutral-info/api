from api.v1.search import keywords, items


class Application(keywords.Application, items.Application):

    # design api function,
    def __init__(self):
        super(Application, self).__init__()
