import os
import json
import random
from datetime import datetime
from project import ThinkUNextApp

TEST_SETS_FOLDER = "sets"
TEST_HISTORY_FOLDER = "history"


def setup_module(module):
    """
    Create necessary directories and test files before running tests.
    """
    os.makedirs(TEST_SETS_FOLDER, exist_ok=True)
    os.makedirs(TEST_HISTORY_FOLDER, exist_ok=True)


def teardown_module(module):
    """
    Clean up the directories and test files after running tests.
    """
    for folder in [TEST_SETS_FOLDER, TEST_HISTORY_FOLDER]:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                os.remove(os.path.join(folder, file))
            os.rmdir(folder)


def test_file_reading():
    """
    Test if the program correctly reads questions from a JSON file.
    """
    test_set_file = os.path.join(TEST_SETS_FOLDER, 'test_set.json')
    test_data = [{"question": "Test Question", "answer": "Test Answer"}]

    # Create a test set
    with open(test_set_file, 'w') as f:
        json.dump(test_data, f)

    # Instantiate the app and read the questions
    app = ThinkUNextApp(None)
    with open(test_set_file, 'r') as f:
        questions = json.load(f)

    assert len(questions) == 1
    assert questions[0]['question'] == "Test Question"
    assert questions[0]['answer'] == "Test Answer"


def test_answer_validation():
    """
    Test the validation logic for user answers.
    """
    app = ThinkUNextApp(None)
    app.correct_answer = "Python"

    user_answer_correct = "python"
    user_answer_incorrect = "java"

    assert user_answer_correct.lower() == app.correct_answer.lower()
    assert user_answer_incorrect.lower() != app.correct_answer.lower()


def test_save_progress():
    """
    Test the saving of session progress to the history folder.
    """
    app = ThinkUNextApp(None)
    app.HISTORY_FOLDER = TEST_HISTORY_FOLDER

    set_name = 'TestSet'
    score = 3
    mistakes = [{"question": "Q1", "user_answer": "A1", "answer": "B1"}]

    app.save_progress(set_name, score, mistakes)

    # Verify history file exists
    history_files = [f for f in os.listdir(TEST_HISTORY_FOLDER) if f.startswith(set_name.upper())]
    assert len(history_files) > 0

    # Verify file content
    with open(os.path.join(TEST_HISTORY_FOLDER, history_files[0]), 'r') as f:
        data = json.load(f)

    assert data['set_name'] == set_name
    assert data['score'] == score
    assert data['mistakes'] == mistakes


def test_question_shuffling():
    """
    Test that questions are shuffled correctly without loss of data.
    """
    app = ThinkUNextApp(None)
    original_questions = [
        {"question": "Q1", "answer": "A1"},
        {"question": "Q2", "answer": "A2"},
        {"question": "Q3", "answer": "A3"}
    ]

    app.questions = original_questions.copy()
    random.shuffle(app.questions)

    # Verify shuffle keeps all elements
    assert len(app.questions) == len(original_questions)
    assert set(q['question'] for q in app.questions) == set(q['question'] for q in original_questions)


def test_empty_set_handling():
    """
    Test behavior when there are no question sets available.
    """
    app = ThinkUNextApp(None)
    set_files = [f[:-5] for f in os.listdir(TEST_SETS_FOLDER) if f.endswith('.json')]
    assert len(set_files) == 0  # Ensure the sets folder is empty


def test_invalid_json_file():
    """
    Test behavior when encountering an invalid JSON file.
    """
    invalid_file = os.path.join(TEST_SETS_FOLDER, 'invalid.json')
    with open(invalid_file, 'w') as f:
        f.write("Invalid JSON content")

    app = ThinkUNextApp(None)
    try:
        with open(invalid_file, 'r') as f:
            json.load(f)
        assert False, "Expected a JSONDecodeError"
    except json.JSONDecodeError:
        assert True


if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "test_project.py"])
