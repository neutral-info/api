from api.v1.schema.keywords import (
    NewsList,
)


class App(search.Application):
    # design api interface
    def __init__(self):
        super(App, self).__init__()
        # register endpoints
        self.api.get("/")(self.main)
        print("app data{}".format(self.keyword))
        self.api.get("/v1/search", response_model=NewsList)(self.keyword)

app = App().api
