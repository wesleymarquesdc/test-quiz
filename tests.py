import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=-1)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_remove_choice():
    question = Question(title='q1')

    question.add_choice('a')

    question.remove_choice_by_id(question.choices[0].id)

    assert len(question.choices) == 0

def test_remove_choice_invalid():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.remove_choice_by_id(1)

def test_remove_all_choices():
    question = Question(title='q1')

    question.add_choice('a')
    question.add_choice('b')

    question.remove_all_choices()

    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='q1')

    question.add_choice('a')
    question.add_choice('b')

    questionA = question.choices[0]
    questionB = question.choices[1]

    question.set_correct_choices([questionA.id])

    assert questionA.is_correct == True
    assert questionB.is_correct == False

def test_set_correct_choices_invalid():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.set_correct_choices([1])

def test_set_correct_choices_empty():
    question = Question(title='q1')

    question.set_correct_choices([])

def test_correct_selected_choices_empty():
    question = Question(title='q1')

    question.add_choice('a', True)

    correct_selected_choices = set(question.correct_selected_choices([]))

    assert set() == correct_selected_choices

def test_correct_selected_choices_correct():
    question = Question(title='q1')

    question.add_choice('a', True)
    question.add_choice('b')

    questionA = question.choices[0]

    correct_selected_choices = set(question.correct_selected_choices([questionA.id]))

    assert {questionA.id} == correct_selected_choices

def test_correct_selected_incorrect():
    question = Question(title='q1')

    question.add_choice('a', True)
    question.add_choice('b')

    questionB = question.choices[1]

    correct_selected_choices = set(question.correct_selected_choices([questionB.id]))

    assert set() == correct_selected_choices

@pytest.fixture
def data():
    return Question(title='q1', max_selections=2)

def test_correct_selected_choices_multiple_correct(data):
    data.add_choice('a', True)
    data.add_choice('b', True)

    questionA = data.choices[0]
    questionB = data.choices[1]

    correct_selected_choices = set(data.correct_selected_choices([questionA.id, questionB.id]))

    assert {questionA.id, questionB.id} == correct_selected_choices


def test_correct_selected_choices_partial(data):
    data.add_choice('a', True)
    data.add_choice('b', True)

    questionA = data.choices[0]

    correct_selected_choices = set(data.correct_selected_choices([questionA.id]))

    assert {questionA.id} == correct_selected_choices