import json

from aiohttp import web

from test_service.db.executor import db


class Author(web.View):
    async def get(self, request):
        author_id = request.match_info['id']
        if author_id:
            sql = '''
                SELECT * FROM authors WHERE %(author_id)s
            '''
            result = db.execute(sql, {'author_id': author_id})
        else:
            sql = '''
                SELECT * FROM authors
            '''
            result = db.execute(sql)
        return web.Response(json=json.dumps(result))
