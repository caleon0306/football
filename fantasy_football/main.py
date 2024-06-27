#required libraries
from fastapi import FastAPI, Request, Form, Cookie,status
from fastapi.responses import HTMLResponse,JSONResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from backend import *
#app is set to FastAPI
app = FastAPI()
app.mount("/frontend/static", StaticFiles(directory="frontend/static"), name="static")

#templates is a variable to the folder named to directory
templates = Jinja2Templates(directory="frontend/templates")

#root directory used for login page
@app.get("/")
async def login(request:Request, loginError=""):
    return templates.TemplateResponse("login.html", context ={"request":request, "loginError":loginError})

#attempt to login
@app.post("/")
async def login(request:Request, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    result = login(username, password)
    print(result)

#sign up page
@app.get("/signUp")
async def login(request:Request, signUpError=""):
    return templates.TemplateResponse("signUp.html", context ={"request":request, "signUpError":signUpError})