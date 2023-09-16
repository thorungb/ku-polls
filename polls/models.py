import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """
    Represents a poll question.

    Attributes:
        question_text (str): The text of the question.
        pub_date (datetime): The date when the question was published.
        end_date (datetime): The date when the question ends (optional).
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField(
        'ending date published',
        null=True,
        blank=True
    )

    def __str__(self):
        """
        Returns a string representation of the question.
        """
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """
        Checks if the question was published recently.
        Returns True if the question was published within the last day,
        False otherwise.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        Checks if the question is currently published.
        Returns True if the question is published, False otherwise.
        """
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """
        Checks if voting is allowed for the question.
        Returns True if voting is allowed, False otherwise.
        """
        now = timezone.now()
        if not self.is_published():
            return False
        if self.end_date is None:
            return True
        else:
            return now <= self.end_date


class Choice(models.Model):
    """
    Represents a choice for a poll question.

    Attributes:
        question (Question): The question associated with the choice.
        choice_text (str): The text of the choice.
        votes (int): The number of votes received for the choice.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        Returns a string representation of the choice.
        """
        return self.choice_text