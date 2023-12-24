import json

from aiohttp import web

from sqlalchemy.exc import IntegrityError

from models import Base, Session, Announcement, engine



def get_http_error(http_error_class, message):
    return http_error_class(
        text=json.dumps({"error": message}), content_type="application/json")



app = web.Application()

async def orm_cntx(app: web.Application):
    print("START")
    async with engine.begin() as con:

        # await con.run_sync(Base.metadata.drop_all)
        await con.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()
    print("SHUT DOWN")


@web.middleware
async def session_middleware(reqest: web.Request, handler):
    async with Session() as session:
        reqest["session"] = session
        response = await handler(reqest)

        return response


app.cleanup_ctx.append(orm_cntx)

app.middlewares.append(session_middleware)


async def get_ann(ann_id: int, session: Session) -> Announcement:
    ann = await session.get(Announcement, ann_id)
    if ann is None:
        raise get_http_error(web.HTTPNotFound, "Announcement not found")

    return ann



class AnnView(web.View):

    @property
    def session(self) -> Session:
        return self.request["session"]


    @property
    def ann_id(self) -> int:
        return int(self.request.match_info["ann_id"])


    async def get(self):

        ann = await get_ann(self.ann_id, self.session)

        return web.json_response(
            {
                "id": ann.id,
                "title": ann.title,
                "description": ann.description,
                "creation_time": ann.creation_time.isoformat(),
                "owner": ann.title
            }
        )


    async def post(self):
        json_data = await self.request.json()

        ann = Announcement(**json_data)

        try:
            self.session.add(ann)
            await self.session.commit()

        except IntegrityError as err:
            raise get_http_error(web.HTTPConflict, "Announcement already exists")

        return web.json_response({"id": ann.id})



    async def delete(self):
        ann = await get_ann(self.ann_id, self.session)

        await self.session.delete(ann)
        await self.session.commit()

        return web.json_response({"status": "deleted"})



app.add_routes(
    [
        web.get("/ann/{ann_id:\d+}/", AnnView),
        web.delete("/ann/{ann_id:\d+}/", AnnView),
        web.post("/ann/", AnnView),
    ]
)



if __name__ == "__main__":
    web.run_app(app)
