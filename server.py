#!/usr/bin/env python3
import asyncio
from aiohttp import web
import requests

async def addr_to_geo(request):
	addr	= request.rel_url.query['addr']
	content = addr	
	return web.Response(text=content,content_type="text/html")

async def call_check(request):	
	content = "ok"	
	return web.Response(text=content,content_type="text/html")


app = web.Application()
app.router.add_route('GET', '/addr_to_geo', call_addr_to_geo)
app.router.add_route('GET', '/check', call_check)

loop = asyncio.get_event_loop()
handler = app.make_handler()
f = loop.create_server(handler, port='8081')
srv = loop.run_until_complete(f)

print('serving on', srv.sockets[0].getsockname())
try:
	loop.run_forever()
except KeyboardInterrupt:
	print("serving off...")
finally:
	loop.run_until_complete(handler.finish_connections(1.0))
	srv.close()