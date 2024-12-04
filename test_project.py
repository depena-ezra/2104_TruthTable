import os
import json
import pytest
from datetime import datetime
from your_program import ThinkUNextApp

USER_SETS = 'sets'
HISTORY_FOLDER = 'history'

@pytest.fixture
def mock_file_operations(monkeypatch):
    def mock_open(path, mode):
        if path.endswith(".json"):
            return {'set_name': 'test_set', 'score': 5, 'mistakes': []}
        else:
            raise FileNotFoundError
    monkeypatch.setattr("builtins.open", mock_open)

def test_read_questions(mock_file_operations):
    set_name = "test_set"
    set_file = os.path.join(USER_SETS, f"{set_name}.json")
    with open(set_file, 'r') as f:
        data = json.load(f)
    assert data['set_name'] == "test_set"
    assert data['score'] == 5

def test_save_progress():
    app = ThinkUNextApp(None)
    set_name = "test_set"
    with open(os.path.join('sets', f"{set_name}.json"), 'w') as f:
        json.dump(questions, f)

    shuffled_questions = shuffle_questions(set_name)

    # Ensure length remains unchanged
    assert len(shuffled_questions) == len(questions), "Shuffling changed the length of the list"

    # Check if the questions remain, even after shuffling
    assert any(q['question'] == "Q1" for q in shuffled_questions), "Question 'Q1' not found in shuffled list"
    assert any(q['question'] == "Q2" for q in shuffled_questions), "Question 'Q2' not found in shuffled list"

    # Test if the order has changed (this is a simple check, the order should not be the same)
    assert questions != shuffled_questions, "Questions were not shuffled"

# Test save_history function
def test_save_history():
    cleanup_history()  # Clean up history folder before test
    cleanup_sets()  # Clean up sets folder before the test

    score = 2
    questions = [{"question": "Q1", "answer": "A1"}]

    save_history(score, questions)

    history_files = [f for f in os.listdir('history') if f.endswith('.json')]
    assert len(history_files) > 0, "History file was not created"

    with open(os.path.join('history', history_files[0]), 'r') as f:
        history_data = json.load(f)

    assert history_data['score'] == score, f"Expected score {score}, but got {history_data['score']}"
    assert len(history_data['mistakes']) == len(questions), "Mismatch in number of mistakes"

    # Clean up after the test
    os.remove(os.path.join('history', history_files[0]))  # Clean up history file

# Run the tests
if __name__ == "__main__":
    pytest.main(["-q", "--tb=line"])  # The "-q" is for quiet mode, "--tb=line" gives simple traceback
