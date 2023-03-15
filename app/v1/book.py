import json

from aiohttp import web

from test_service.db.executor import db


class Book(web.View):
    async def get(self, request):
        author_id = request.match_info['id']
        sql = '''
            SELECT * FROM books WHERE %(author_id)s
        '''
        result = db.execute(sql, {'book_id': author_id})
        return web.Response(json=json.dumps(result))