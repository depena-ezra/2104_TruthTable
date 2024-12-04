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
    score = 5
    mistakes = []
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    history_filename = os.path.join(HISTORY_FOLDER, f"{set_name.upper()}_session_{timestamp}.json")
    app.save_progress(set_name, score, mistakes)
    assert os.path.exists(history_filename)

def test_validate_answer():
    app = ThinkUNextApp(None)
    app.correct_answer = "Correct Answer"
    user_answer = "correct answer"
    assert app.validate_answer(user_answer) == "Correct!"
    user_answer = "incorrect answer"
    assert app.validate_answer(user_answer) == "Incorrect! The correct answer was: Correct Answer"

def test_show_review_result():
    app = ThinkUNextApp(None)
    app.questions = [{"question": "What is 2 + 2?", "answer": "4"}]
    app.mistakes = []
    app.show_review_result("test_set")
    assert app.mistakes == []
    app.mistakes = [{"question": "What is 2 + 2?", "user_answer": "3", "answer": "4"}]
    app.show_review_result("test_set")
    assert len(app.mistakes) == 1

def test_create_review_panel():
    app = ThinkUNextApp(None)
    review_panel = app.create_review_panel()
    assert isinstance(review_panel, tk.Frame)
    assert "Choose a Set to Review" in [child.cget("text") for child in review_panel.winfo_children()]