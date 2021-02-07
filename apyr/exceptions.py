class EndpointException(Exception):
    pass


class TooManyEndpointsException(EndpointException):
    def __init__(self):
        self.message = "There are too many endpoints matching the conditions."
        super().__init__(self.message)


class NoEndpointsException(EndpointException):
    def __init__(self):
        self.message = "There are no endpoints matching the conditions."
        super().__init__(self.message)
