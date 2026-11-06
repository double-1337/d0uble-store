import os
import aiosqlite
from aiohttp import web

@web.middleware
async def cors_middleware(request, handler):
    if request.method == "OPTIONS":
        response = web.Response()
    else:
        response = await handler(request)

    response.headers["Access-Control-Allow-Origin"] = (
        "https://double-1337.github.io"
    )
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"

    return response


async def get_products(request):
    async with aiosqlite.connect("shop.db") as db:
        cursor = await db.execute(
            "SELECT id, name, description, price FROM products"
        )
        products = await cursor.fetchall()

    return web.json_response([
        {
            "id": p[0],
            "name": p[1],
            "description": p[2],
            "price": p[3]
        }
        for p in products
    ])


app = web.Application(middlewares=[cors_middleware])
app.router.add_get("/products", get_products)
app.router.add_route("OPTIONS", "/products", lambda request: web.Response())

port = int(os.environ.get("PORT", 8001))
web.run_app(app, host="0.0.0.0", port=port)