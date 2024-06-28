import bcrypt
import backend.queryRunner as qr

#create account credentials for a user
def create_account(username = "", password = "", confirmPassword=""):
    #check username and password requierments
    username_result = username_requierments(username)
    if type(username_result) == str:
        return username_result
    password_result = password_requierments(password, confirmPassword)
    if type(password_result) == str:
        return password_result
    #create a new account with user info
    query = f"""INSERT INTO user_info
    (username, password)
    VALUES('{username}', '{storedPass(password)}');"""
    qr.run_commit(query)

    #fetch the id of the acout created
    query = f"""SELECT user_id
    FROM user_info
    WHERE username = '{username}'"""
    return qr.fetch_one(query)[0]

#login function to attempt to login to credentials
def login(username="", password=""):
    #make sure credentials entered
    if username == "":
        return "Username required."
    if password == "":
        return "Password required."

    #run a query to get row with matching username and password
    query = f"""SELECT user_id, password
    FROM user_info
    WHERE username = '{username}';"""
    result = qr.fetch_one(query)

    #check to see if credentials match an account
    if result == None:
        return "Invalid username/password."
    
    #check encoded given password with encoded stored password
    #True means match and return what is wanted
    if(bcrypt.checkpw(str(password).encode(), result[1].encode())):
        print(result[0])
        return result[0]

#create a league for league_info
def create_league(user_id, name="", size=2, price=0,firstPlace=0, secondPlace=0, thirdPlace=0,
                  highestPointsSeason=0, highestScoringWeek=0,highestScoreWeekly=0,numWeeklyPayouts=0):
    #check to ensure name meets requierments
    nameCheck = league_name_requierments(name)
    if type(nameCheck) == str:
        return nameCheck
    #check to ensure league size meets requierments
    print("SIZE:",size)
    print("TYPE:", type(size))
    sizeCheck = league_size_requierments(size)
    if type(sizeCheck) == str:
        return sizeCheck
    #check to ensure prices meet requierments
    priceCheck = league_price_requierments(price, firstPlace, secondPlace, thirdPlace, highestPointsSeason, highestScoringWeek, highestScoreWeekly)
    if type(priceCheck) == str:
        return priceCheck
    
    #add the essential league info
    query = f"""INSERT INTO league_info
    ("owner_id", "league_name", "size", "team_price", "first_payout", "second_payout", "third_payout", "highest_points_season_payout", "highest_scoring_week_payout", "highest_points_weekly_payout", "number_weekly_payouts")
    VALUES('{user_id}', '{name}', '{size}', '{price}', '{firstPlace}', '{secondPlace}', '{thirdPlace}', '{highestPointsSeason}', '{highestScoringWeek}', '{highestScoreWeekly}', '{numWeeklyPayouts}');"""
    qr.run_commit(query)
    
    #run a query to get the id of the league created by the owner
    #league id is stored in result
    query = f"""SELECT MAX(league_id)
    FROM league_info
    WHERE "owner_id" = '{user_id}';"""
    result = qr.fetch_one(query)[0]
    update_pots(result)
    return result

#recalculate the money for the league
def update_pots(league_id):
    #query to select the columns that deal with money
    query = f"""SELECT size, team_price, first_payout, second_payout, third_payout, highest_points_season_payout, highest_scoring_week_payout, highest_points_weekly_payout, number_weekly_payouts, extra_payout
    FROM league_info
    WHERE "league_id" = '{league_id}';"""
    result = qr.fetch_one(query)
    #assign variables to the result for easier readability
    size = result[0]
    price = result[1]
    firstPayout = result[2]
    secondPayout = result[3]
    thirdPayout = result[4]
    highPointSeason = result[5]
    highPointWeek = result[6]
    highWeeklyPoint = result[7]
    numWeeklyPayout = result[8]
    extraPayout = 0 if result[9] == None else result[9]
    #calculate dependent variables
    totalPot = size * price
    assignedPot = firstPayout + secondPayout + thirdPayout + highPointSeason + highPointWeek + (highWeeklyPoint * numWeeklyPayout) + extraPayout
    unassignedPot = totalPot - assignedPot

    #update league pot
    query = f"""UPDATE league_info
    SET "total_pot" = '{totalPot}', "assigned_pot" = '{assignedPot}', "unassigned_pot" ='{unassignedPot}', "extra_payout" = '{extraPayout}'
    WHERE "league_id" = '{league_id}';"""
    qr.run_commit(query)

#check requierments for username
#String returned if not valid
#True returned if valid
def username_requierments(username = ""):
    if username == "":
        return "Username required."
    if len(username) > 29:
        return "Username must be less than 30 characters."
    
    #run a query to get all accounts with same username
    query = f"""SELECT *
    FROM user_info
    WHERE username = '{username}';"""
    result = qr.fetch_one(query)
    #check if account exists with username
    if result == None:
        return True
    return "Username already in use."

#check requierments for password
#String returned if not vaild
#True returned if valid
def password_requierments(password = "", confirmPassword = ""):
    if password == "":
        return "Password required."
    if len(password) > 29:
        return "Password must be less than 30 characters."
    if password != confirmPassword:
        return "Passwords do not match."
    return True

#check to ensure league has a name
def league_name_requierments(name = ""):
    if name == "":
        return "Enter a league name."
    if len(name) > 29:
        return "League name must be less than 30 characters."
    return True

#requierments for a league size
def league_size_requierments(size):
    if size < 2:
        return "League size must be greater than 1."
    return True

#requierments for team prices
#ensure no negative or non-integer
def league_price_requierments(*prices):
    for price in prices:
        if price < 0:
            return "Prices cannot be less than 0."
        if type(price) != int:
            return "Prices must be a whole number."
    return True

#hash the given password and return its decoded result
#result used to store in database
def storedPass(password):
    hashedPass = bcrypt.hashpw(str(password).encode(), bcrypt.gensalt())
    return hashedPass.decode()

#return username based on user id      
def get_username(user_id):
    query = f"""SELECT username
    FROM user_info
    WHERE "user_id" = '{user_id}';"""
    return qr.fetch_one(query)[0]