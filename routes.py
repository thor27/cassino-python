import handlers



routes = [
    ("/", "SimpleHandler"),
    ("/vote", "VoteHandler"),
    ("/result", "ResultHandler"),
]

class AppRoutes(object):
    def __init__(self, app):
        self.handlers = []
        for route, handler_name in routes:
            handler_class = getattr(handlers, handler_name)
            handler = handler_class(app)
            for method in handler.methods:
                getattr(app.router, "add_" + method)(route, getattr(handler, method))
