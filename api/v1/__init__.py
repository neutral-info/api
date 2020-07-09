from api.v1.schema import output_data

from api.v1 import endpoints


class Application(endpoints.Application):
    # design api function,
    def __init__(self):
        super(Application, self).__init__()
        self.api.get("/api/v1", response_model=output_data.News)(self.data_v1)
