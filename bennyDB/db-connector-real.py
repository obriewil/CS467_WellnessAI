import psycopg2
from psycopg2 import Error
import datetime



DB_HOST = ""  # e.g., "34.123.45.67"
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""
DB_PORT = 5432 # Default PostgreSQL port


class wellness_ai_db:
    def __init__(self):
        self.db = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        self.cursor = self.db.cursor()
        self.create_sql_possible_preferences_table()
        self.create_sql_user_preferences_table()
        self.create_four_week_plan()
        self.create_sql_create_ideal_plan_table()
        self.create_log_table()
        print("initialized")


    #generic run-query function
    def run_query(self, query, *query_args):
        do_it = self.cursor.execute(query, [*query_args])
        self.db.commit()
        return do_it

    # full list of selectable goal preferences
    def create_sql_possible_preferences_table(self):
        query = """CREATE TABLE IF NOT EXISTS preferences_list (
        preference_id SERIAL PRIMARY KEY,
        preference_name VARCHAR(255)
        );
        """
        self.run_query("DROP TABLE preferences_list;")
        self.run_query(query)
        self.build_possible_pref_table()
        

    #build possible preferences table
    def build_possible_pref_table(self):
        self.run_query("INSERT INTO preferences_list(preference_name) VALUES ('sleep');" )
        self.run_query("INSERT INTO preferences_list(preference_name) VALUES ('meditation');" )
        self.run_query("INSERT INTO preferences_list(preference_name) VALUES ('outside time');" )
        self.run_query("INSERT INTO preferences_list(preference_name) VALUES ('strength training');" )
        self.run_query("INSERT INTO preferences_list(preference_name) VALUES ('cardiovascular training');" )
        self.run_query("INSERT INTO preferences_list(preference_name) VALUES ('mobility training');" )
        self.run_query("INSERT INTO preferences_list(preference_name) VALUES ('protein intake');")
        self.run_query("INSERT INTO preferences_list(preference_name) VALUES ('fruit and veggie intake');")
        self.run_query("INSERT INTO preferences_list(preference_name) VALUES ('hydration');")

    # stores user goal preferences/ranking 
    def create_sql_user_preferences_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS user_priorities (
            user_preference_id SERIAL PRIMARY KEY,
            user_rating INT,
            preference_name VARCHAR(255) NOT NULL REFERENCES preferences_list(preference_name),
            user_ref_pref_id INT,
            CONSTRAINT fk_preference_id FOREIGN KEY (user_ref_pref_id) REFERENCES preferences_list(preference_id)
        );
        """
        self.run_query(query)

    
    # calendar for planning ideal program
    def create_sql_create_ideal_plan_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS user_program (
            row_id SERIAL PRIMARY KEY,
            date DATE NOT NULL
            
            );
        """
        self.run_query(query)

    # four week running ideal program
    def create_four_week_plan(self):
        query = """
        CREATE TABLE IF NOT EXISTS user_four_week (
            row_id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            week INT NOT NULLL
            );
            """
        self.run_query(query)

    
    # date/activity pairing for goal calendar, stores activities and what user goals those activities work towards.
    def create_sql_activity_planning_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS daily_activities_ref(
            row_id SERIAL PRIMARY KEY,
            program_row_id INT NOT NULL,
            activity_name VARCHAR(255) NOT NULL,
            activity_addresses_goal INT REFERENCES user_priorities(user_ref_pref_id),
            CONSTRAINT fk_row_id FOREIGN KEY (program_row_id) REFERENCES user_program(row_id)
        );
        """
        self.run_query(query)


    # date/activity pairing for goal calendar, stores activities and what user goals those activities work towards.
    def create_sql_activity_planning_table_four_week(self):
        query = """
        CREATE TABLE IF NOT EXISTS daily_activities_ref(
            row_id SERIAL PRIMARY KEY,
            program_row_id INT NOT NULL,
            activity_name VARCHAR(255) NOT NULL,
            activity_addresses_goal INT REFERENCES user_priorities(user_ref_pref_id),
            CONSTRAINT fk_row_id FOREIGN KEY (program_row_id) REFERENCES user_four_week(row_id)
        );
        """
        self.run_query(query)

    #creates daily log table
    def create_log_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS daily_log_table(
        row_id SERIAL PRIMARY KEY,
        log_date DATE NOT NULL
        )
        """
        self.run_query(query)

    #create daily_log_activity table
    def create_daily_log_activity(self):
        query = """
        CREATE TABLE IF NOT EXISTS log_activities(
        row_id SERIAL PRIMARY KEY,
        daily_log_id INT NOT NULL,
        activity_name VARCHAR(255) NOT NULL,
        activity_addresses_goal INT REFERENCES user_priorities(user_ref_pref_id),
        CONSTRAINTS fk_log FOREIGN KEY (daily_log_id) REFERENCES daily_log_table(row_id)
        );
        """
        self.run_query(query)

    #sets user preferences, takes as input a ranking integer and a goal name input
    def set_preferences(self, pref_name, pref_rank):
        self.run_query("INSERT INTO user_priorities (user_rating, preference_name) VALUES (?, ?);", pref_name, pref_rank)

    #add row to daily log
    def add_daily_log_row(self, today_date):
        self.run_query("INSERT INTO daily_log_table (log_date) VALUES (?);", today_date)

    # adds a row to the four week plan
    def add_four_week_plan_row(self, input_date, input_week):
        self.run_query("INSERT INTO user_four_week (date, week) VALUES (?,?);", input_date, input_week)

    #add row to ideal plan
    def add_ideal_plan_row(self, input_date):
        self.run_query("INSERT INTO user_program (date) VALUES (?);", input_date)

    #build four weeks worth of rows in four week plan
    def build_full_four_week_plan(self):
        day=0
        week=1
        while(day<=28):
            day+=1
            week += (day%7)
            self.add_four_week_plan_row(day, week)

    #


main_db = wellness_ai_db()