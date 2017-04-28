from aiohttp import web

from controllers import VoteController
from controllers import ResultController


class ResultHandler(object):
    methods=("post",)
    def __init__(self, app):
        self.app = app
        self.controller = ResultController()

    async def post(self, request):
        data = await request.json()
        await self.controller.insert(data)
        return web.Response(text="OK")


class SimpleHandler(object):
    methods=("get",)
    def __init__(self, app):
        self.app = app

    async def get(self, request):
        return web.Response(text="Cassino. In Python.")


class VoteHandler(object):
    methods=("post",)
    def __init__(self, app):
        self.app = app
        self.controller = VoteController(app)

    async def post(self, request):
        data = await request.json()
        await self.controller.insert(data)
        return web.Response(text="OK")
