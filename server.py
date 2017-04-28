from aiohttp import web
from routes import AppRoutes


app = web.Application()
AppRoutes(app)
web.run_app(app)
