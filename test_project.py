import pytest
import json
import random
import os
from project import add_question, shuffle_questions, save_history

# Clean up the history folder before testing (ensure it doesn't accumulate)
def cleanup_history():
    history_files = [f for f in os.listdir('history') if f.endswith('.json')]
    for file in history_files:
        os.remove(os.path.join('history', file))

# Clean up the sets folder before testing
def cleanup_sets():
    set_files = [f for f in os.listdir('sets') if f.endswith('.json')]
    for file in set_files:
        os.remove(os.path.join('sets', file))

# Test add_question function
def test_add_question():
    cleanup_sets()  # Clean up before the test
    add_question("What is 2+2?", "4")

    set_name = "test_set"  # Default name for the test
    questions = shuffle_questions(set_name)

    # Assert that the question was added
    assert any(q['question'] == "What is 2+2?" for q in questions), "Question not found in shuffled list"

# Test shuffle_questions function
def test_shuffle_questions():
    cleanup_sets()  # Clean up before the test
    questions = [{"question": "Q1", "answer": "A1"}, {"question": "Q2", "answer": "A2"}]

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
