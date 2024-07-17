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
    return templates.TemplateResponse(name="dashboard.html", context={"user_id":user_id, "request":request})

#page to create a new league
@app.get("/createLeague")
async def createLeaguePage(request:Request, user_id: Annotated[str | None, Cookie()] = None, createLeagueError = "", values = {}):
    return templates.TemplateResponse("createLeague.html", context={"user_id":user_id, "request":request, "createLeagueError":createLeagueError, "values":values})

#attempt to create a new league
@app.post("/createLeague")
async def createLeagueAttempt(request:Request, user_id: Annotated[str | None, Cookie()], leagueName: Annotated[str, Form()] = "", size: Annotated[int, Form()] = 0, price: Annotated[int, Form()] = 0,firstPayout: Annotated[int, Form()] = 0,secondPayout: Annotated[int, Form()] = 0,thirdPayout: Annotated[int, Form()] = 0,highestPointsSeason: Annotated[int, Form()] = 0,highestSingleWeek: Annotated[int, Form()] = 0,highestPointsPerWeek: Annotated[int, Form()] = 0,numWeeklyPayouts: Annotated[int, Form()] = 0):
    result = create_league(user_id,leagueName,size,price,firstPayout,secondPayout,thirdPayout,highestPointsSeason,highestSingleWeek,highestPointsPerWeek,numWeeklyPayouts)
    if (type(result)) == str:
        values = {"leagueName": leagueName, "size": size, "price": price, "firstPayout": firstPayout, "secondPayout": secondPayout, "thirdPayout": thirdPayout,
                  "highestPointsSeason":highestPointsSeason,"highestSingleWeek":highestSingleWeek,"highestPointsPerWeek":highestPointsPerWeek,"numWeeklyPayouts":numWeeklyPayouts}
        return await createLeaguePage(request, user_id, result, values)
    response = RedirectResponse("leagueHome/"+ str(result), status_code=status.HTTP_303_SEE_OTHER)
    return response

#page to enter information to join a league
@app.get("/joinLeague")
async def joinLeague(request:Request, user_id: Annotated[str | None, Cookie()] = None, values={}, errorMessage=""):
    return templates.TemplateResponse(name="joinLeague.html", context = {"user_id": user_id, "request":request, "values":values, "errorMessage":errorMessage})

#attempt to join a leauge
@app.post("/joinLeague")
async def joinLeagueAttempt(request:Request,user_id: Annotated[str | None, Cookie()], league_name: Annotated[str, Form()] = "", league_id: Annotated[int, Form()] = 0):
    result = join_league(user_id, league_id, league_name)
    if result == True:
        response = RedirectResponse("leagueHome/" + str(league_id), status_code=status.HTTP_303_SEE_OTHER)
        return response
    values = {"league_name": league_name, "league_id": league_id}
    return await joinLeague(request,user_id,values, errorMessage = result)
    

#league home page
#id of the league attempting to be accessed is passed
#check if the cookie of the user is in the league
@app.get("/leagueHome/{league}")
async def leaguePage(league:int, request:Request,user_id: Annotated[str | None, Cookie()] = None):
    if check_in_league(user_id, league):
        return templates.TemplateResponse("leagueHome.html", context={"user_id":user_id, "league":league, "request":request})
    else:
        return "Unable to access league"

#returns a league information based on league id passed
@app.post("/leagueInfo/{league}")
async def leaguePage(league:int ,resquest:Request, user_id:Annotated[str | None, Cookie()] = None):
    result = get_league_info(league)
    return JSONResponse(content = result)

#get all user leagues information
@app.post("/userLeagues")
async def userLeagues(request:Request, user_id:Annotated[str | None, Cookie()] = None):
    result = get_joined_leagues(user_id)
    return JSONResponse(content = result)

#get logout page
@app.get("/logout")
async def logout(request:Request, user_id: Annotated[str | None, Cookie()] = None):
    return templates.TemplateResponse("logout.html", context={"request":request})

#attempt to logout and clear cookies
@app.post("/logout")
async def logout(request:Request, user_id: Annotated[str | None, Cookie()] = None):
    print("IN LOGOUT POST")
    response = RedirectResponse("", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="user_id",)
    return response