#required libraries
from fastapi import FastAPI, Request, Form, Cookie,status
from fastapi.responses import HTMLResponse,JSONResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated

#app is set to FastAPI
app = FastAPI()
app.mount("/frontend/static", StaticFiles(directory="frontend/static"), name="static")

#templates is a variable to the folder named to directory
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/")
async def login(request:Request, loginError=""):
    return templates.TemplateResponse("login.html", context ={"request":request, "loginError":loginError})