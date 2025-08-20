from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api import api_router


app = FastAPI()
templates = Jinja2Templates(directory="templates/")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/data/{data_id}")
def serve_data_page(request: Request):
    pass



app.include_router(api_router(), prefix="/api")
