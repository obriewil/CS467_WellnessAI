import psycopg2
from psycopg2 import Error
import datetime
import requests



DB_HOST = ""  # e.g., "34.123.45.67"
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""
DB_PORT = 5432 # Default PostgreSQL port
FRONTEND_URL = "http://localhost:5173/"
BENNY_AI_URL = "http://127.0.0.1:8001"


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
        self.create_check_in_question_table()
        print("initialized")

##########  Database Manipulation Functions  ######################
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
        
    #build daily reporting form
    def daily_report_form(self):
        query = """
        CREATE TABLE IF NOT EXISTS log_questions(
        row_id SERIAL PRIMARY KEY,
        question VARCHAR(255),
        response INT
        );"""
        self.run_query(query)


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
            week INT NOT NULL
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
            activity_addresses_goal INT REFERENCES user_priorities(user_preference_id),
            CONSTRAINT fk_row_id FOREIGN KEY (program_row_id) REFERENCES user_program(row_id)
        );
        """
        self.run_query(query)


    # date/activity pairing for goal calendar, stores activities and what user goals those activities work towards.
    def create_sql_activity_planning_table_four_week(self):
        query = """
        CREATE TABLE IF NOT EXISTS daily_activities_ref_four(
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
        log_date DATE NOT NULL,
        sleep_quality VARCHAR(255),
        stress_level VARCHAR(255),
        nutrition VARCHAR(255)
        );
        """
        self.run_query(query)

    #create daily_log_activity table
    def create_daily_log_activity(self):
        query = """
        CREATE TABLE IF NOT EXISTS log_activities(
        row_id SERIAL PRIMARY KEY,
        daily_log_id INT NOT NULL,
        activity_name VARCHAR(255) NOT NULL,
        user_success INT NOT NULL,
        activity_addresses_goal INT REFERENCES user_priorities(user_ref_pref_id),
        CONSTRAINTS fk_log FOREIGN KEY (daily_log_id) REFERENCES daily_log_table(row_id)
        );
        """
        self.run_query(query)

    #create daily check in questions table
    def create_check_in_question_table(self):
        self.run_query("DROP TABLE questions;")
        query = """
        CREATE TABLE IF NOT EXISTS questions(
        row_id SERIAL PRIMARY KEY,
        question_text VARCHAR(255)
        );"""
        self.run_query(query)
        
        self.run_query("INSERT INTO questions (question_text) VALUES ('Ready for our daily check in? How did you feel about your nutrition choices today?');")
        self.run_query("INSERT INTO questions (question_text) VALUES ('And how would you rate your sleep last night?');")
        self.run_query("INSERT INTO questions (question_text) VALUES ('Now for fitness. Did you complete your planned fitness activity today?');")
        self.run_query("INSERT INTO questions (question_text) VALUES ('Finally, let's check in on your well-being. How would you rate your stress levels today?');")
        self.run_query("INSERT INTO questions (question_text) VALUES ('Thanks for completing our check in. You're doing great!')")


    #sets user preferences, takes as input a ranking integer and a goal name input
    def set_preferences(self, pref_name, pref_rank):
        self.run_query("INSERT INTO user_priorities (user_rating, preference_name) VALUES (?, ?);", pref_name, pref_rank)

    

    # adds a row to the four week plan
    def add_four_week_plan_row(self, input_date, input_week):
        self.run_query("INSERT INTO user_four_week (date, week) VALUES (?,?);", input_date, input_week)

    #add row to ideal plan
    def add_ideal_plan_row(self, input_date):
        self.run_query("INSERT INTO user_program (date) VALUES (?);", input_date)

    #build four weeks worth of rows in four week plan
    def build_full_four_week_plan(self):
        self.run_query("DROP TABLE IF EXISTS user_four_week;")
        self.run_query("DROP TABLE IF EXISTS user_activity_ref_four;")
        self.create_four_week_plan() #drop existing table and reinitialize an empty one
        self.create_sql_activity_planning_table_four_week()
        now = datetime.datetime.now()
        input_date = now
        day = 0
        week=1
        while(day<=28): #build 28 new rows for new 4 week plan, with ascending primary keys corresponding to days from today
            week += (day%7)
            day+=1
            input_date += datetime.timedelta(days=1)
            self.add_four_week_plan_row(input_date, week)

    #adds newly generated 4 week plan to full program
    def add_four_weeks_to_existing_program(self):
        now = datetime.datetime.now()
        input_date = now
        day = 0
        while(day<=28): #adds 28 new rows to ideal plan table
            day+=1
            input_date += datetime.timedelta(days=1)
            self.add_ideal_plan_row(input_date)

    #gets user priority pk based on goal name
    def get_user_priority_pk(self, goal_name):
        goal_pk = self.run_query("SELECT user_preference_id FROM user_priorities WHERE preference_name=(?);", goal_name)
        return goal_pk

    #adds an activity to the full ideal program
    def add_activity_to_full_ideal_program(self, input_date, activity_name):
        main_prog_row_id = self.run_query("SELECT row_id FROM user_program WHERE date=(?);", input_date)
        activity_pk = self.get_user_priority_pk(activity_name)
        self.run_query("INSERT INTO daily_activities_ref (program_row_id,activity_name, activity_addresses_goal) VALUES (?,?,?);", main_prog_row_id, activity_name, activity_pk)
    
    #add an activity to four week program for specific date
    def add_activity_to_four_week_program(self, input_date, activity_name):
        main_prog_row_id = self.run_query("SELECT row_id FROM user_program WHERE date=(?);", input_date)
        activity_pk = self.get_user_priority_pk(activity_name)
        self.run_query("INSERT INTO daily_activities_ref_four (program_row_id,activity_name, activity_addresses_goal) VALUES (?,?,?);", main_prog_row_id, activity_name, activity_pk)

    #adds an activity to both four week program and full ideal program
    def add_programmed_activity(self, input_date, activity_name):
        self.add_activity_to_four_week_program(input_date, activity_name)
        self.add_activity_to_full_ideal_program(input_date, activity_name)
        
    #add row to daily log and populate planned activities
    def add_daily_log_row(self, today_date):
        self.run_query("INSERT INTO daily_log_table (log_date) VALUES (?);", today_date)
        self.cursor.execute("SELECT row_id FROM daily_log_table WHERE log_date = (?);", today_date)
        log_pk_id = self.cursor.fetchone()
        self.cursor.execute("SELECT row_id FROM user_program WHERE date=(?);", today_date)
        main_prog_row_id = self.cursor.fetchone()
        self.cursor.execute("SELECT * FROM daily_activity_ref WHERE program_row_id=(?);", main_prog_row_id)
        planned_activities = self.cursor.fetchall()
        for activity in planned_activities:
            self.run_query("INSERT INTO log_activities (daily_log_id, activity_name, user_success, activity_addresses_goal) VALUES (?,?, 0,?);", log_pk_id, activity[2], activity[3])

    #updates user success from default of 0 to 1 if user successfully completed activity
    def update_user_success_daily_log(self, today_date, activity_name, user_success):
        log_pk_id = self.run_query("SELECT row_id FROM daily_log_table WHERE log_date = (?);", today_date)
        activity_row_id = self.run_query("SELECT row_id FROM log_activities WHERE (daily_log_id=(?)) AND (activity_name=(?));", log_pk_id, activity_name)
        self.run_query("UPDATE log_activities SET user_success = (?) WHERE row_id = (?);", user_success, activity_row_id)

    #retrieve log form responses for today 
    def get_form_responses_for_benny(self):
        now = datetime.datetime.now()
        now = now.date()
        self.cursor.execute("""SELECT (sleep_quality, stress_level, nutrition) FROM daily_log_table WHERE log_date=(?);""", now)
        log_data = self.cursor.fetchone() 
        return log_data
    
    #returns form questions for frontend
    def get_form_questions_daily_checkin(self):
        self.cursor.execute("""SELECT * FROM questions;""")
        questions = self.cursor.fetchall()
        return questions
    
#################  API communication functions  #########################

    #send data to frontend
    def send_data_to_frontend(self, frontend_data):
        try:    
            data = requests.post(FRONTEND_URL, data=frontend_data)
            data.raise_for_status() #error handling
        except requests.exceptions.ConnectionError as e:
            print(f"Error connecting to Frontend API at {FRONTEND_URL}: {e}")
            return {"error": "Frontend API connection failed"}
        except requests.exceptions.Timeout as e:
            print(f"Frontend API request timed out: {e}")
            return {"error": "Frontend API timeout"}
        except requests.exceptions.RequestException as e:
            print(f"Error calling Frontend API: {e}")
            return {"error": f"Frontend API request failed: {e}"}


    #send data to benny ai
    def send_data_to_benny(self, ai_data):
        try:    
            data = requests.post(BENNY_AI_URL, data=ai_data)
            data.raise_for_status() #error handling
        except requests.exceptions.ConnectionError as e:
            print(f"Error connecting to Benny API at {BENNY_AI_URL}: {e}")
            return {"error": "Benny API connection failed"}
        except requests.exceptions.Timeout as e:
            print(f"Benny API request timed out: {e}")
            return {"error": "Benny API timeout"}
        except requests.exceptions.RequestException as e:
            print(f"Error calling Benny API: {e}")
            return {"error": f"Benny API request failed: {e}"}
         

main_db = wellness_ai_db()