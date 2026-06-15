"""
Django Shell ORM Examples — Tutorial 02
Run: python manage.py shell

>>> from polls.models import Question, Choice
>>> from django.utils import timezone

# Create
>>> q = Question(question_text="What's new?", pub_date=timezone.now())
>>> q.save()
>>> q.id  # 1

# Read
>>> Question.objects.all()
>>> Question.objects.filter(id=1)
>>> Question.objects.filter(question_text__startswith="What")
>>> Question.objects.get(pk=1)

# Related objects
>>> q.choice_set.all()
>>> q.choice_set.create(choice_text="Not much", votes=0)
>>> q.choice_set.create(choice_text="The sky", votes=0)
>>> q.choice_set.count()  # 2

# Filter across relationships
>>> current_year = timezone.now().year
>>> Choice.objects.filter(question__pub_date__year=current_year)

# Delete
>>> c = q.choice_set.filter(choice_text__startswith="Just")
>>> c.delete()
"""