# Citations: 
# Referencing DB manager skeleton accessed from https://www.pythonguis.com/examples/kivy-to-do-app/,
# my own work based off of this db manager I produced for CS361, 
# and CS361 course materials. 

import datetime
import requests
import sqlite3
import pathlib


FRONTEND_URL = "http://localhost:5173/"
BENNY_AI_URL = "http://127.0.0.1:8001"

DATABASE_PATH = pathlib.Path(__file__).parent / "BennyDB.sqlite3"


class wellness_ai_db:
    def __init__(self):
        self.db = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.db.cursor()
        self.create_sql_possible_preferences_table()
        self.create_sql_user_preferences_table()
        self.create_sql_create_ideal_plan_table()
        self.create_log_table()
        self.create_check_in_question_table()
        print("initialized")


    #generic run-query function
    def run_query(self, query, *query_args):
        do_it = self.cursor.execute(query, [*query_args])
        self.db.commit()
        return do_it


##########  Database TABLE BUILD Functions  ######################

    # full list of selectable goal preferences
    def create_sql_possible_preferences_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS preferences_list (
            preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
            preference_name VARCHAR(255)
        );
        """
        self.run_query("DROP TABLE IF EXISTS preferences_list;")
        self.run_query(query)
        self.build_possible_pref_table()


    #build daily reporting form
    def daily_report_form(self):
        query = """
            CREATE TABLE IF NOT EXISTS log_questions(
            row_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question VARCHAR(255),
            response INTEGER
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
            user_preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_rating INTEGER,
            user_ref_pref_id INTEGER NOT NULL,
            FOREIGN KEY (user_ref_pref_id) REFERENCES preferences_list(preference_id)

        );
        """
        self.run_query(query)

    
    # calendar for planning ideal program, will contain column for identifying which rows are in the four week display
    def create_sql_create_ideal_plan_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS user_program (
            row_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date VARCHAR(255) NOT NULL,
            activity_name VARCHAR(255) NOT NULL,
            activity_addresses_goal INTEGER NOT NULL,
            in_curr_four_week INTEGER NOT NULL,
            FOREIGN KEY (activity_addresses_goal) REFERENCES user_priorities(user_preference_id)
        );
        """
        self.run_query(query)


    #creates daily log table
    def create_log_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS daily_log_table(
            row_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_program_row_id INTEGER NOT NULL,
            log_date VARCHAR(255) NOT NULL,
            sleep_quality VARCHAR(255),
            stress_level VARCHAR(255),
            nutrition VARCHAR(255),
            activity_complete INTEGER NOT NULL,
            activity_name VARCHAR(255),
            activity_addresses_goal INTEGER NOT NULL,
            FOREIGN KEY (activity_addresses_goal) REFERENCES user_priorities(user_ref_pref_id),
            FOREIGN KEY (user_program_row_id) REFERENCES user_program(row_id)
        );
        """
        self.run_query(query)


    #create daily check in questions table
    def create_check_in_question_table(self):
        self.run_query("DROP TABLE IF EXISTS questions;")
        query = """
            CREATE TABLE IF NOT EXISTS questions(
            row_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text VARCHAR(255)
        );"""
        self.run_query(query)
        self.run_query("INSERT INTO questions (question_text) VALUES ('Ready for our daily check in? How did you feel about your nutrition choices today?');")
        self.run_query("INSERT INTO questions (question_text) VALUES ('And how would you rate your sleep last night?');")
        self.run_query("INSERT INTO questions (question_text) VALUES ('Now for fitness. Did you complete your planned fitness activity today?');")
        self.run_query("INSERT INTO questions (question_text) VALUES ('Finally, let us check in on your well-being. How would you rate your stress levels today?');")
        self.run_query("INSERT INTO questions (question_text) VALUES ('Thanks for completing our check in. You are doing great!')")


    #create table for conversation history
    def create_chat_history_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS chat_history (
            row_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date VARCHAR(255) NOT NULL
        );"""
        self.run_query(query)


    #create table for entries into conversation history
    #0 for user, 1 for benny
    #sequence number starts at 1 for conversation and increments
    def create_chat_history_entry_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS chat_history_entries (
            row_id INTEGER PRIMARY KEY AUTOINCREMENT,
            fk_row_id INTEGER NOT NULL,
            sequence_number INTEGER NOT NULL,
            user_or_benny INTEGER NOT NULL,
            entry_text TEXT NOT NULL,
            FOREIGN KEY (fk_row_id) REFERENCES chat_history(row_id)
        );"""
        self.run_query(query)

############### DATABASE ADD AND UPDATE FUNCTIONS ###############

    #add row to chat history table
    def insert_row_chat_history_main(self, input_date):
        self.run_query("INSERT INTO chat_history (date) VALUES (?);", input_date)


    #add entry into chat history table
    def add_chat_entry(self, input_date, sequence_number, user_or_benny, chat_text):
        get_pk = self.run_query("SELECT row_id FROM chat_history WHERE date = (?);", input_date)
        fk = get_pk.fetchone()
        self.run_query("INSERT INTO chat_history_entries (fk_row_id, sequence_number, user_or_benny, entry_text) VALUES (?,?,?,?);", fk, sequence_number, user_or_benny, chat_text)

        
    #sets user preferences, takes as input a ranking integer and a goal name input
    def set_preferences(self, pref_name, pref_rank):
        self.run_query("INSERT INTO user_priorities (user_rating, preference_name) VALUES (?, ?);", pref_name, pref_rank)

    # remove instances of current four week plan when building a new one
    def reset_four_week_status(self):
        self.run_query("UPDATE user_program SET in_curr_four_week = (?) WHERE in_curr_four_week = (?)", 0, 1)

    # adds a row to the four week plan
    def add_four_week_plan_row(self, input_date):
        self.run_query("INSERT INTO user_program (date, in_curr_four_week) VALUES (?,?);", input_date,1)


    #build four weeks worth of rows in four week plan
    def build_full_four_week_plan(self):
        self.reset_four_week_status()
        now = datetime.datetime.now()
        now = now.date()
        input_date = now
        day = 0
        while(day<=28): #build 28 new rows for new 4 week plan, with ascending primary keys corresponding to days from today
            day+=1
            input_date += datetime.timedelta(days=1)
            nowstring = now.strftime("%m/%d/%Y")
            self.add_four_week_plan_row(nowstring)


    #adds an activity to the full ideal program
    def add_activity_to_full_ideal_program(self, input_date, activity_name):
        main_prog_row_id = self.run_query("SELECT row_id FROM user_program WHERE date=(?);", input_date)
        main_prog_row_id = main_prog_row_id[1]
        activity_pk = self.get_user_priority_pk(activity_name)
        self.run_query("INSERT INTO daily_activities_ref (program_row_id,activity_name, activity_addresses_goal) VALUES (?,?,?);", (main_prog_row_id, activity_name, activity_pk))
    

    #adds an activity to both four week program and full ideal program
    def add_programmed_activity(self, input_date, activity_name):
        self.add_activity_to_full_ideal_program(input_date, activity_name)

        
    #add row to daily log and populate planned activities (test indicies)
    def add_daily_log_row(self, today_date):
        program_get = self.user_program_day_get(today_date)
        main_prog_row_id = program_get[0]
        main_prog_activity = program_get[2]
        main_prog_activity_reason = program_get[3]
        self.run_query("INSERT INTO daily_log_table (user_program_row_id, log_date, activity_complete, activity_name, activity_addresses_goal) VALUES (?)", main_prog_row_id, today_date, 0, main_prog_activity, main_prog_activity_reason)


    #updates user success from default of 0 to 1 if user successfully completed activity
    def update_user_success_daily_log(self, date):
        self.run_query("UPDATE daily_log_table SET activity_complete=(?) WHERE log_date=(?);", 1, date)


    #undoes the user success logging above if needed for error recovery
    def reset_user_success_daily_log(self, date):
        self.run_query("UPDATE daily_log_table SET activity_complete=(?) WHERE log_date=(?);", 0, date)

    #add ranked goal to goal table
    #can be updated to use preference pk instead of name
    def add_ranked_goal(self, preference_name, preference_rank):
        pk = self.run_query("SELECT preference_id FROM preferences_list WHERE preference_name = (?);", preference_name)
        fk = pk.fetchone()
        self.run_query("INSERT INTO user_priorities (user_rating, user_ref_pref_id) VALUES (?,?);", preference_rank, fk)

    
    #delete a row from user priorities table
    def delete_ranked_goal(self, preference_name):
        pk = self.run_query("SELECT preference_id FROM preferences_list WHERE preference_name = (?);", preference_name)
        fk = pk.fetchone()
        self.run_query("DELETE FROM user_priorities WHERE user_ref_pref_id = (?);", fk)

    
    #update user ranking of existing priority
    def delete_ranked_goal(self, preference_name, preference_rank):
        pk = self.run_query("SELECT preference_id FROM preferences_list WHERE preference_name = (?);", preference_name)
        fk = pk.fetchone()
        self.run_query("UPDATE user_priorities SET user_rating = (?) WHERE user_ref_pref_id = (?);", preference_rank, fk)

############ DATABASE GET FUNCTIONS ##################

    #get chat history main table pk given date
    def fetch_main_chat_history_pk(self, input_date):
        pk = self.run_query("SELECT row_id FROM chat_history WHERE date = (?);", input_date)
        return pk.fetchone()


    #gets all chat entries for a certain date and orders by sequence
    def fetch_chat_logs_by_date(self, input_date):
        row_id = self.fetch_main_chat_history_pk(input_date)
        chats = self.run_query("SELECT * FROM chat_history_entries WHERE fk_row_id = (?) ORDER BY sequence_number ASCENDING;", row_id)
        return chats.fetchall()
   

    #gets user priority pk based on goal name
    def get_user_priority_pk(self, goal_name):
        goal_pk = self.run_query("SELECT * FROM user_priorities WHERE preference_name=(?);", goal_name)
        return goal_pk.fetchone()

    

    #gets user preference ratings for benny decision making
    def get_all_user_preferences(self):
        preferences = self.run_query("SELECT * FROM user_priorities;")
        return preferences.fetchall()


    #get all user priorities
    def get_user_priorities(self):
        prios = self.run_query("SELECT * FROM user_priorities;")
        return prios.fetchall()


    #retrieve log form responses for today as dictionary
    def get_form_responses_for_benny(self):
        now = datetime.datetime.now()
        now = now.date()
        nowstring = now.strftime("%m/%d/%Y")
        log_answers_para_bennward = self.run_query("SELECT * FROM daily_log_table WHERE log_date=(?);", nowstring)
        return log_answers_para_bennward.fetchall()


    #returns form questions for frontend as dictionary
    def get_form_questions_daily_checkin(self):
        questions = self.run_query("SELECT * FROM questions ORDER BY row_id ASCENDING;")
        return questions.fetchall()


    #returns 4 week plan
    def get_four_week_plan(self):
        four_week_plan_get = self.run_query("SELECT * FROM user_program WHERE in_curr_four_week=(?) ORDER BY row_id ASCENDING;", 1)
        return four_week_plan_get.fetchall()


    #gets a row from the daily log based on date
    def daily_log_row_fetch(self, date):
        log_get = self.run_query("SELECT * FROM daily_log_table WHERE log_date = (?);", date)
        return log_get.fetchone()
    

    #gets a row from the user program based on date
    def user_program_day_get(self, date):
        program_get = self.run_query("SELECT * FROM user_program WHERE date = (?);", date)
        return program_get.fetchone()

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
         
#### Main DB Backend ####
main_db = wellness_ai_db()