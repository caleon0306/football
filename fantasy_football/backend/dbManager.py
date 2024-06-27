import queryRunner as qr

#create user_info table
def create_user_info_table():   
    #create table design
    query = """CREATE TABLE IF NOT EXISTS user_info(
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(70) UNIQUE,
        password VARCHAR(70) NOT NULL
        );"""
    qr.run_commit_query(query)

def create_league_info_table():
    #create table design
    query = """CREATE TABLE IF NOT EXISTS league_info(
        league_id SERIAL PRIMARY KEY,
        owner_id INT NOT NULL,
        league_name VARCHAR(70) NOT NULL,
        max_size INT NOT NULL,
        team_price DEC(7,2) NOT NULL,
        total_pot DEC(9,2),
        pot_remaining DEC(9,2),
        pot_paidout DEC(9,2),
        first_payout DEC(9,2),
        second_payout DEC(9,2),
        third_payout DEC(9,2),
        highest_points_season_payout DEC(9,2),
        highest_scoring_week_payout DEC(9,2),
        highest_points_weekly_payout DEC(9,2),
        number_weekly_payouts INT,
        extra_payout DEC(9,2),
        FOREIGN KEY (owner_id) REFERENCES user_info(user_id)
    );"""
    qr.run_commit_query(query)

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
        extra_payout DEC(9,2),
        FOREIGN KEY (user_id) REFERENCES user_info(user_id),
        FOREIGN KEY (league_id) REFERENCES league_info(league_id)
    );"""
    qr.run_commit_query(query)

#drop a table based on table name passed
def drop_table(table = ""):
    #check to ensure table is passed
    if table == "":
        return
    query = f"""DROP TABLE IF EXISTS {table};"""
    qr.run_commit_query(query)

#drop all tables then add them back
def reset_all_tables():
    drop_table("league_players")
    drop_table("league_info")
    drop_table("user_info")
    create_user_info_table()
    create_league_info_table()
    create_leage_players_table()

def get_rows_table(table = ""):
    if table == "":
        return
    query= f"""SELECT *
    FROM {table};"""
    return qr.fetch_all(query)

#if __name__ == "__main__":
