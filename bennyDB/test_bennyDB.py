"""
File: test_bennyDB.py
Author: William O'Brien
Description: This script demonstrates tests for the bennyDB. Specifically,
    it runs tests for the db_connector_real.py file. This file also runs
    automated on any pushes or merges to the main branch per the file
    .github/workflows/bennydb_test.yml
"""

# Import your database connector
from db_connector_real import wellness_ai_db


def test_update_user_success_daily_log():
    """
    Very simple test for updating user success daily log.
    The test will add data, update it, check if updated, delete.
    """

    # Initialize database connector and define test date
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

    # Check that information was inserted into the database
    assert row is not None, "Row not found in database"

    # Based on the table schema activity_complete should be at index 6
    assert row[6] == 1, f"activity_complete should be 1, got {row[6]}"

    # Delete test data
    db.run_query("DELETE FROM daily_log_table WHERE log_date = ?;", test_date)

    # Verify deletion
    verify_result = db.run_query("SELECT * FROM daily_log_table WHERE log_date = ?;", test_date)
    verify_row = verify_result.fetchone()
    assert verify_row is None, "Row should be deleted but still exists"

    # Cleanup
    db.db.close()


def test_get_all_user_preferences():
    """
    Test get_all_user_preferences function
    """

    # Initialize database connector
    db = wellness_ai_db()

    # Add test data directly (avoiding the buggy add_ranked_goal)
    pref_result = db.run_query("SELECT preference_id FROM preferences_list WHERE preference_name = ?;", "meditation")
    pref_row = pref_result.fetchone()
    assert pref_row is not None, "Could not find 'meditation' preference in preferences_list"
    pref_id = pref_row[0]

    # Insert sample data into user priorities with a unique test rating
    test_rating = 5  # Using a unique rating for testing
    db.run_query("INSERT INTO user_priorities (user_rating, user_ref_pref_id) VALUES (?, ?);", test_rating, pref_id)

    # Verify the data was inserted
    verify_insert = db.run_query("SELECT * FROM user_priorities WHERE user_rating = ? AND user_ref_pref_id = ?;", test_rating, pref_id)
    verify_row = verify_insert.fetchone()
    assert verify_row is not None, f"Test data was not inserted into user_priorities table"

    # Call the function
    result = db.get_all_user_preferences()

    # Assert statement to check that data was inserted
    assert result is not None, "Result should not be None"
    assert len(result) > 0, "Result should contain data"

    # Check that our specific test data exists in the result
    # Based on debug output: format is (user_preference_id, user_rating, user_ref_pref_id)
    found_test_data = False
    for row in result:
        if row[1] == test_rating and row[2] == pref_id:
            found_test_data = True
            # Verify we have a valid user_preference_id (should be a positive integer)
            assert isinstance(row[0], int) and row[0] > 0, f"Expected positive integer for user_preference_id, got {row[0]}"
            break

    assert found_test_data, f"Could not find test data with rating={test_rating} and pref_id={pref_id} in results"

    # Cleanup
    db.run_query("DELETE FROM user_priorities WHERE user_rating = ?;", test_rating)
    db.db.close()


def test_get_user_priorities():
    """
    Test get_user_priorities function
    """

    # Initialize database connector
    db = wellness_ai_db()

    # Add test data directly
    pref_result = db.run_query("SELECT preference_id FROM preferences_list WHERE preference_name = ?;", "sleep")
    pref_id = pref_result.fetchone()[0]

    # Insert sample data into user priorities with a unique test rating
    test_rating = 9  # Using a unique rating for testing
    db.run_query("INSERT INTO user_priorities (user_rating, user_ref_pref_id) VALUES (?, ?);", test_rating, pref_id)

    # Call the function
    result = db.get_user_priorities()

    # Assert statement to check that data was inserted
    assert result is not None, "Result should not be None"
    assert len(result) > 0, "Result should contain data"

    # Check that we have the expected columns: user_preference_id, user_rating, user_ref_pref_id
    first_row = result[0]
    assert len(first_row) == 3, f"Expected 3 columns, got {len(first_row)}"

    # Check that our specific test data exists in the result
    found_test_data = False
    for row in result:
        if row[1] == test_rating and row[2] == pref_id:
            found_test_data = True
            # Verify we have a valid user_preference_id (should be a positive integer)
            assert isinstance(row[0], int) and row[0] > 0, f"Expected positive integer for user_preference_id, got {row[0]}"
            break

    assert found_test_data, f"Could not find test data with rating={test_rating} and pref_id={pref_id} in results"

    # Cleanup
    db.run_query("DELETE FROM user_priorities WHERE user_rating = ?;", test_rating)
    db.db.close()


def test_get_form_responses_for_benny():
    """
    Test get_form_responses_for_benny function
    """

    # Initialize database connector
    db = wellness_ai_db()

    # Add test data for today's date
    import datetime
    today = datetime.datetime.now().date().strftime("%m/%d/%Y")
    test_activity_name = "test_activity_for_benny"

    db.run_query("""INSERT INTO daily_log_table
                    (user_program_row_id, log_date, activity_complete, activity_name, activity_addresses_goal)
                    VALUES (?, ?, ?, ?, ?);""",
                 1, today, 1, test_activity_name, 1)

    # Call the function
    result = db.get_form_responses_for_benny()

    # Assert statement to check that data was inserted
    assert result is not None, "Result should not be None"
    assert len(result) > 0, "Result should contain data"

    # Check that our specific test data exists in the result
    found_test_data = False
    for row in result:
        # Check if this row contains our test activity
        if any(test_activity_name in str(field) for field in row if field is not None):
            found_test_data = True
            # Verify the row contains today's date
            assert any(today in str(field) for field in row if field is not None), f"Expected today's date '{today}' in row, but not found"
            break

    assert found_test_data, f"Could not find test data with activity_name='{test_activity_name}' and date='{today}' in results"

    # Cleanup
    db.run_query("DELETE FROM daily_log_table WHERE log_date = ? AND activity_name = ?;", today, test_activity_name)
    db.db.close()
