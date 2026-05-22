from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()


from oder_router import oder_routers
from auth_router import auth_routers

app.include_router(oder_routers)
app.include_router(auth_routers)


@app.get("/")
def read_root():
    return {"Hello": "World"}
 