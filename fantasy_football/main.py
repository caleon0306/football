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
async def signUpPage(request:Request, signUpError="", username = ""):
    return templates.TemplateResponse("signUp.html", context ={"request":request, "signUpError":signUpError, "username":username})

#attempt to sign up an account
@app.post("/signUp")
async def signUpAttempt(request:Request, username: Annotated[str, Form()] = "", password: Annotated[str, Form()] = "", passwordConfirm: Annotated[str, Form()] = ""):
    result = create_account(username, password, passwordConfirm)
    if type(result) == str:
        return await signUpPage(request, result, username)
    response = RedirectResponse("dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user_id", value = result)
    return response

#main user homepage
@app.get("/dashboard")
async def dashboard(request:Request, user_id: Annotated[str | None, Cookie()] = None):
    return templates.TemplateResponse(name="dashboard.html", context={"username":user_id, "request":request})

#page to create a new league
@app.get("/createLeague")
async def createLeaguePage(request:Request, user_id: Annotated[str | None, Cookie()] = None, createLeagueError = "", values = {}):
    return templates.TemplateResponse("createLeague.html", context={"username":user_id, "request":request, "createLeagueError":createLeagueError, "values":values})

#attempt to create a new league
@app.post("/createLeague")
async def createLeagueAttempt(request:Request, user_id: Annotated[str | None, Cookie()], leagueName: Annotated[str, Form()] = "", size: Annotated[int, Form()] = 0, price: Annotated[int, Form()] = 0,firstPayout: Annotated[int, Form()] = 0,secondPayout: Annotated[int, Form()] = 0,thirdPayout: Annotated[int, Form()] = 0,highestPointsSeason: Annotated[int, Form()] = 0,highestSingleWeek: Annotated[int, Form()] = 0,highestPointsPerWeek: Annotated[int, Form()] = 0,numWeeklyPayouts: Annotated[int, Form()] = 0):
    result = create_league(user_id,leagueName,size,price,firstPayout,secondPayout,thirdPayout,highestPointsSeason,highestSingleWeek,highestPointsPerWeek,numWeeklyPayouts)
    if (type(result)) == str:
        values = {"leagueName": leagueName, "size": size, "price": price, "firstPayout": firstPayout, "secondPayout": secondPayout, "thirdPayout": thirdPayout,
                  "highestPointsSeason":highestPointsSeason,"highestSingleWeek":highestSingleWeek,"highestPointsPerWeek":highestPointsPerWeek,"numWeeklyPayouts":numWeeklyPayouts}
        return await createLeaguePage(request, user_id, result, values)
    response = RedirectResponse("leagueHome", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="league_id",value = result)
    return response

#league home page
@app.get("/leagueHome")
async def leaguePage(request:Request,user_id: Annotated[str | None, Cookie()] = None,league_id: Annotated[str | None, Cookie()] = None):
    return templates.TemplateResponse("leagueHome.html", context={"user_id":user_id, "league_id":league_id, "request":request})

#returns a league information
@app.post("/leagueInfo")
async def leaguePage(resquest:Request, user_id:Annotated[str | None, Cookie()] = None, league_id:Annotated[str | None, Cookie()] = None):
    result = get_league_info(league_id)
    return JSONResponse(content = result)

#get league information
@app.post("/userLeagues")
async def userLeagues(request:Request, user_id:Annotated[str | None, Cookie()] = None, league_id:Annotated[str | None, Cookie()] = None):
    result = get_joined_leagues(user_id)
    return JSONResponse(content = result)