import json

from aiohttp import web

from test_service.db.executor import db


class Rating(web.View):
    async def get(self, request):
        obj_type = request.match_info['type']
        sql = f'''
            SELECT * FROM %s WHERE %%(rating > 90)s AND LIMIT 10
        '''.format(type)
        result = db.execute(sql, {'book_id': obj_type})
        return web.Response(json=json.dumps(result))
