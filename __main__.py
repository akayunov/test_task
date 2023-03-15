from aiohttp import web
from aiohttp.web import middleware
from test_service.app.v1.author import Author
from test_service.app.v1.auth import Auth
from test_service.app.v1.book import Book
from test_service.app.v1.admin import Admin
from test_service.app.v1.rating import Rating


@middleware
async def middleware_1(request, handler):
    '''do validation of jwt token'''
    '''do authorization'''


app = web.Application(middlewares=[middleware_1, ])
app.add_routes('*', r'/v1/{path:auth}', Auth)
app.add_routes('*', r'/v1/{path:author}/{id:\d+}?', Author)
app.add_routes('*', r'/v1/{path:author}/{id:\d+}/book', Book)
app.add_routes('*', r'/v1/{path:rating}/{type:[book|author]}', Rating)
app.add_routes('*', r'/v1/{path:admin}', Admin)
