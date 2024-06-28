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
    qr.run_commit_query(query)

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
def create_league(user_id, name, size, price,firstPlace=0, secondPlace=0, thirdPlace=0,
                  highestPointsSeason=0, highestScoringWeek=0,highestScoreWeekly=0,numWeeklyPayouts=0):
    totalPot = size * price
    potRemaining = totalPot - firstPlace - secondPlace - thirdPlace -highestPointsSeason - highestScoreWeekly
    query = f"""INSERT INTO league_info
    ("owner_id");"""

#check requierments for username
#String returned if not valid
#True returned if valid
def username_requierments(username = ""):
    if username == "":
        return "Username required."
    if len(username) > 29:
        return "Username is too long."
    
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
        return "Password is too long."
    if password != confirmPassword:
        return "Passwords do not match."
    return True

#hash the given password and return its decoded result
#result used to store in database
def storedPass(password):
    hashedPass = bcrypt.hashpw(str(password).encode(), bcrypt.gensalt())
    return hashedPass.decode()
        