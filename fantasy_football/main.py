#required libraries
from fastapi import FastAPI, Request, Form, Cookie,status
from fastapi.responses import HTMLResponse,JSONResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from backend.funcs import *
#app is set to FastAPI
app = FastAPI()
app.mount("/frontend/static", StaticFiles(directory="frontend/static"), name="static")

#templates is a variable to the folder named to directory
templates = Jinja2Templates(directory="frontend/templates")

#root directory used for login page
@app.get("/")
async def loginPage(request:Request, loginError="", username = ""):
    return templates.TemplateResponse("login.html", context ={"request":request, "loginError":loginError, "username":username})

#attempt to login
@app.post("/")
async def loginAttempt(request:Request, username: Annotated[str, Form()] = "", password: Annotated[str, Form()] = ""):
    result = login(username, password)
    #check result to see if credentials are correct
    if type(result)== str:
        return await loginPage(request, result, username)
    response=RedirectResponse("dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user_id", value=result)
    return response

#sign up page
@app.get("/signUp")
async def signUpPage(request:Request, signUpError=""):
    return templates.TemplateResponse("signUp.html", context ={"request":request, "signUpError":signUpError})

#main user homepage
@app.get("/dashboard")
async def dashboard(request:Request, userid: Annotated[str | None, Cookie()] = None):
    return templates.TemplateResponse(name="dashboard.html", context={"username":userid, "request":request})