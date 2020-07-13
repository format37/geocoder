#!/usr/bin/env python3
import asyncio
from aiohttp import web
import requests
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

async def call_addr_to_geo(request):
	addr	= request.rel_url.query['addr']
	df = pd.DataFrame({'name': [
		addr
	]})
	geolocator = Nominatim(user_agent="ice_geo")
	geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
	df['location'] = df['name'].apply(geocode)
	df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)

	content = '00000000;00000000'
	for i in df['point']:
		if i!=None:
			content = str(int(i[0]*1000000))+';'+str(int(i[1]*1000000))
			break
		
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
