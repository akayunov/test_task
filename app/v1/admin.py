import json

from aiohttp import web

from test_service.db.executor import db


class Admin(web.View):
    async def post(self, request):
        '''do some admin stuff'''

