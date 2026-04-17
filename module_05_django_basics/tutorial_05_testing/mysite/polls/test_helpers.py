import datetime
from django.utils import timezone
from .models import Question


def create_question(question_text, days):
    """
    Create a question with the given text and published the given
    number of days offset to now (negative for past, positive for future).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)