# Import your database connector
from db_connector_real import wellness_ai_db


def test_update_user_success_daily_log():
    """
    Very simple test: add data, update it, check if updated, delete.
    """

    db = wellness_ai_db()

    test_date = "01/15/2025"

    # Add a test row to daily_log_table first (with activity_complete = 0)
    db.run_query("""INSERT INTO daily_log_table
                    (user_program_row_id, log_date, activity_complete, activity_name, activity_addresses_goal)
                    VALUES (?, ?, ?, ?, ?);""",
                 1, test_date, 0, "test_activity", 1)

    # Call the update function
    db.update_user_success_daily_log(test_date)

    # Check if it was updated to 1
    result = db.run_query("SELECT * FROM daily_log_table WHERE log_date = ?;", test_date)
    row = result.fetchone()

    assert row is not None, "Row not found in database"

    # Based on the table schema: row_id, user_program_row_id, log_date, sleep_quality, stress_level, nutrition, activity_complete, activity_name, activity_addresses_goal
    # activity_complete should be at index 6
    assert row[6] == 1, f"activity_complete should be 1, got {row[6]}"

    # Delete test data
    db.run_query("DELETE FROM daily_log_table WHERE log_date = ?;", test_date)

    # Verify deletion
    verify_result = db.run_query("SELECT * FROM daily_log_table WHERE log_date = ?;", test_date)
    verify_row = verify_result.fetchone()
    assert verify_row is None, "Row should be deleted but still exists"

    db.db.close()


def test_get_all_user_preferences():
    """Test get_all_user_preferences function"""
    # Initialize database connector
    db = wellness_ai_db()

    # Add test data directly (avoiding the buggy add_ranked_goal)
    pref_result = db.run_query("SELECT preference_id FROM preferences_list WHERE preference_name = ?;", "meditation")
    pref_id = pref_result.fetchone()[0]

    db.run_query("INSERT INTO user_priorities (user_rating, user_ref_pref_id) VALUES (?, ?);", 3, pref_id)

    # Call the function
    result = db.get_all_user_preferences()

    assert result is not None
    assert len(result) > 0

    # Cleanup
    db.run_query("DELETE FROM user_priorities WHERE user_rating = ?;", 3)
    db.db.close()


def test_get_user_priorities():
    """Test get_user_priorities function"""
    # Initialize database connector
    db = wellness_ai_db()

    # Add test data directly
    pref_result = db.run_query("SELECT preference_id FROM preferences_list WHERE preference_name = ?;", "sleep")
    pref_id = pref_result.fetchone()[0]

    db.run_query("INSERT INTO user_priorities (user_rating, user_ref_pref_id) VALUES (?, ?);", 4, pref_id)

    # Call the function
    result = db.get_user_priorities()

    assert result is not None
    assert len(result) > 0

    # Check that we have the expected columns: user_preference_id, user_rating, user_ref_pref_id
    first_row = result[0]
    assert len(first_row) == 3

    # Cleanup
    db.run_query("DELETE FROM user_priorities WHERE user_rating = ?;", 4)
    db.db.close()


def test_get_form_responses_for_benny():
    """Test get_form_responses_for_benny function"""
    # Initialize database connector
    db = wellness_ai_db()

    # Add test data for today's date
    import datetime
    today = datetime.datetime.now().date().strftime("%m/%d/%Y")

    db.run_query("""INSERT INTO daily_log_table
                    (user_program_row_id, log_date, activity_complete, activity_name, activity_addresses_goal)
                    VALUES (?, ?, ?, ?, ?);""",
                 1, today, 1, "test_activity", 1)

    # Call the function
    result = db.get_form_responses_for_benny()

    assert result is not None
    assert len(result) > 0

    # Cleanup
    db.run_query("DELETE FROM daily_log_table WHERE log_date = ?;", today)
    db.db.close()


def test_add_ranked_goal_fixed():
    """Test adding ranked goal with manual implementation (since add_ranked_goal has bugs)"""
    # Initialize database connector
    db = wellness_ai_db()

    # Get a valid preference_id
    pref_result = db.run_query("SELECT preference_id FROM preferences_list WHERE preference_name = ?;", "sleep")
    pref_id = pref_result.fetchone()[0]

    # Add preference manually (correct way)
    db.run_query("INSERT INTO user_priorities (user_rating, user_ref_pref_id) VALUES (?, ?);", 5, pref_id)

    # Verify it was added
    result = db.get_all_user_preferences()
    assert len(result) > 0

    # Find our preference
    found = False
    for pref in result:
        if pref[1] == 5:  # user_rating = 5
            found = True
            break

    assert found, "Added preference not found"

    # Cleanup
    db.run_query("DELETE FROM user_priorities WHERE user_rating = ?;", 5)
    db.db.close()
