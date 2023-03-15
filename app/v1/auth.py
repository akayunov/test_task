import json

from aiohttp import web

from test_service.db.executor import db


class Auth(web.View):
    async def post(self, request):
        ''' check user passwrd in DB and generate and return jst token'''
        return web.Response(json=json.dumps({'token': some_func_to_generate_token}))
