import queryRunner as qr

#create user_info table
def create_user_info_table():   
    #create table design
    query = """CREATE TABLE IF NOT EXISTS user_info(
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(30) UNIQUE,
        password VARCHAR(60) NOT NULL
        );"""
    qr.run_commit(query)

def create_league_info_table():
    #create table design
    query = """CREATE TABLE IF NOT EXISTS league_info(
        league_id SERIAL PRIMARY KEY,
        owner_id INT NOT NULL,
        league_name VARCHAR(30) NOT NULL,
        size INT NOT NULL,
        team_price INT NOT NULL,
        total_pot INT,
        assigned_pot INT,
        unassigned_pot INT,
        first_payout INT,
        second_payout INT,
        third_payout INT,
        highest_points_season_payout INT,
        highest_scoring_week_payout INT,
        highest_points_weekly_payout INT,
        number_weekly_payouts INT,
        extra_payout INT,
        FOREIGN KEY (owner_id) REFERENCES user_info(user_id)
    );"""
    qr.run_commit(query)

def create_leage_players_table():
    query = """CREATE TABLE IF NOT EXISTS league_players(
        user_id INT NOT NULL,
        league_id INT NOT NULL,
        paid DEC(7,2),
        first BOOLEAN,
        second BOOLEAN,
        third BOOLEAN,
        highest_points_season BOOLEAN,
        highest_scoring_week BOOLEAN,
        number_highest_weekly_points INT,
        extra_won INT,
        FOREIGN KEY (user_id) REFERENCES user_info(user_id),
        FOREIGN KEY (league_id) REFERENCES league_info(league_id)
    );"""
    qr.run_commit(query)

#drop a table based on table name passed
def drop_table(table = ""):
    #check to ensure table is passed
    if table == "":
        return
    query = f"""DROP TABLE IF EXISTS {table};"""
    qr.run_commit(query)

#drop all tables then add them back
def reset_all_tables():
    drop_table("league_players")
    drop_table("league_info")
    drop_table("user_info")
    create_user_info_table()
    create_league_info_table()
    create_leage_players_table()

#get the rows for a table
def get_rows_table(table = ""):
    if table == "":
        return
    query= f"""SELECT *
    FROM {table};"""
    return qr.fetch_all(query)

#if __name__ == "__main__":
    print(get_rows_table("user_info"))