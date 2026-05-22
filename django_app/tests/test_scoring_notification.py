import pytest
from progress.services.scoring_svc import ScoringService


@pytest.mark.django_db
def test_quiz_pass_triggers_notification(enrolled_user, quiz, monkeypatch):
    called_with = []

    def fake_notify(user_id, node_id, node_title):
        called_with.append((user_id, node_id, node_title))

    monkeypatch.setattr("progress.services.scoring_svc.notify_node_unlocked", fake_notify)

    questions = quiz.questions.all()
    answers = {str(q.id): q.answer for q in questions}
    
    result = ScoringService.calculate_quiz_score(
        enrolled_user, quiz.id, answers
    )

    assert isinstance(result, dict)
    assert result["passed"] == True
    assert len(called_with) == 1