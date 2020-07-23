from api.v1 import search
from api.v1.schema.keywords import NewsList


class App(search.Application):
    # design api interface
    def __init__(self):
        super(App, self).__init__()
        # register endpoints
        self.api.get("/api/v1/keyword", response_model=NewsList)(self.keyword)
        self.api.get("/api/v1/item")(self.item)

app = App().api
