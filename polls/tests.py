import datetime

from django.test import TestCase
from django.utils import timezone

# from .models import Question
from django.urls import reverse

from django.contrib.auth.models import User
# from django.contrib.auth import authenticate # to "login" a user using code
from polls.models import Question, Choice, Vote
from mysite import settings


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):

    # unit tests for 'was_published_recently'
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(
            hours=23, minutes=59, seconds=59
        )
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    # unit tests for 'is_published'
    def test_is_published_with_future_pub_date(self):
        """
        is_published return False for questions with a pub_date in the future.
        """
        question = create_question(" ", days=4)
        self.assertEqual(question.is_published(), False)

    def test_is_published_with_the_default_pub_date(self):
        """
        is_published return True for questions with the default pub_date.
        """
        question = create_question(" ", days=0)
        self.assertEqual(question.is_published(), True)

    def test_is_published_with_pub_date_in_the_past(self):
        """
        is_published return True for questions with a pub_date in the past.
        """
        question = create_question(" ", days=-4)
        self.assertEqual(question.is_published(), True)

    # unit tests for 'can_vote'
    def test_can_vote_with_no_end_date(self):
        """
        Can vote if the end_date is null, and the pub_date is in the past.
        """
        question = create_question(question_text=" ", days=-5)
        self.assertTrue(question.can_vote())

    def test_can_vote_within_voting_period(self):
        """
        Can vote if the current date is between the pub_date and the end_date.
        """
        question = create_question(question_text=" ", days=-5)
        question.end_date = timezone.now() + datetime.timedelta(days=5)
        question.save()
        self.assertTrue(question.can_vote())

    def test_cannot_vote_before_pub_date(self):
        """
        Cannot vote if the current date is before the pub_date,
        even if the end_date is in the future.
        """
        question = create_question(question_text=" ", days=5)
        question.end_date = timezone.now() + datetime.timedelta(days=10)
        question.save()
        self.assertFalse(question.can_vote())

    def test_cannot_vote_after_end_date(self):
        """
        Cannot vote if the end_date is in the past.
        """
        question = create_question(question_text=" ", days=-10)
        question.end_date = timezone.now() - datetime.timedelta(days=5)
        question.save()
        self.assertEqual(question.can_vote(), False)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(
            question_text='Future question.',
            days=5
        )
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(
            question_text='Past Question.',
            days=-5
        )
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


"""Tests of authentication."""


class UserAuthTest(TestCase):

    def setUp(self):
        # superclass setUp creates a Client object & initializes test database
        super().setUp()
        self.username = "testuser"
        self.password = "FatChance!"
        self.user1 = User.objects.create_user(
                         username=self.username,
                         password=self.password,
                         email="testuser@nowhere.com"
                         )
        self.user1.first_name = "Tester"
        self.user1.save()
        # we need a poll question to test voting
        q = Question.objects.create(question_text="First Poll Question")
        q.save()
        # a few choices
        for n in range(1, 4):
            choice = Choice(choice_text=f"Choice {n}", question=q)
            choice.save()
        self.question = q

    def test_logout(self):
        """A user can logout using the logout url.

        As an authenticated user,
        when I visit /accounts/logout/
        then I am logged out
        and then redirected to the login page.
        """
        logout_url = reverse("logout")
        # Authenticate the user.
        # We want to logout this user, so we need to associate the
        # user user with a session.  Setting client.user = ... doesn't work.
        # Use Client.login(username, password) to do that.
        # Client.login returns true on success
        self.assertTrue(
              self.client.login(username=self.username, password=self.password)
                       )
        # visit the logout page
        response = self.client.post(logout_url)
        self.assertEqual(302, response.status_code)

        # should redirect us to where? Polls index? Login?
        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL))

    def test_login_view(self):
        """A user can login using the login view."""
        login_url = reverse("login")
        # Can get the login page
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        # Can login using a POST request
        # usage: client.post(url, {'key1":"value", "key2":"value"})
        form_data = {"username": "testuser", "password": "FatChance!"}
        response = self.client.post(login_url, form_data)
        # after successful login, should redirect browser somewhere
        self.assertEqual(302, response.status_code)
        # should redirect us to the polls index page ("polls:index")
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_auth_required_to_vote(self):
        """Authentication is required to submit a vote.

        As an unauthenticated user,
        when I submit a vote for a question,
        then I am redirected to the login page
          or I receive a 403 response (FORBIDDEN)
        """
        vote_url = reverse('polls:vote', args=[self.question.id])

        # what choice to vote for?
        choice = self.question.choice_set.first()
        # the polls detail page has a form, each choice is identified by its id
        form_data = {"choice": f"{choice.id}"}
        response = self.client.post(vote_url, form_data)
        # should be redirected to the login page
        self.assertEqual(response.status_code, 302)  # could be 303
        login_with_next = f"{reverse('login')}?next={vote_url}"
        self.assertRedirects(response, login_with_next)


class VoteTestCase(TestCase):
    def setUp(self):
        """Set up initial data for the vote test cases."""
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )
        self.question = Question.objects.create(
            question_text='Test Question',
            pub_date=timezone.now()
        )
        # Create test choices for the question
        self.choice1 = Choice.objects.create(
            question=self.question,
            choice_text='Choice 1'
        )
        self.choice2 = Choice.objects.create(
            question=self.question,
            choice_text='Choice 2'
        )

    def test_user_can_vote(self):
        """Test that an authenticated user can vote for a choice."""
        self.client.login(username="testuser", password="password123")
        vote_url = reverse('polls:vote', args=[self.question.id])
        # Submit a POST request to vote for choice1
        response = self.client.post(vote_url, {'choice': self.choice1.id})
        # Check if the response status code is a redirect (302)
        self.assertEqual(response.status_code, 302)
        # Check if the user's vote has been recorded in the database
        self.assertTrue(
            Vote.objects.filter(user=self.user, choice=self.choice1).exists())

    def test_user_cannot_vote_twice(self):
        """Test that a user cannot vote for the same question twice."""
        self.client.login(username="testuser", password="password123")
        vote_url = reverse('polls:vote', args=[self.question.id])
        # Submit a POST request to vote for choice1
        # response = self.client.post(vote_url, {'choice': self.choice1.id})
        # Try to vote for choice2 after already voting for choice1
        response2 = self.client.post(vote_url, {'choice': self.choice2.id})
        # Check if the response is a redirect (302) indicating they can't vote
        self.assertEqual(response2.status_code, 302)

    def test_anonymous_user_cannot_vote(self):
        """Test that an anonymous user cannot vote."""
        vote_url = reverse('polls:vote', args=[self.question.id])
        # Submit a POST request to vote for choice1 without logging in
        response = self.client.post(vote_url, {'choice': self.choice1.id})
        # Check if the response is a redirect (302) indicating they can't vote
        self.assertEqual(response.status_code, 302)

    def test_voting_redirects_to_results(self):
        """Test that voting redirects to the results page for the question."""
        self.client.login(username="testuser", password="password123")
        # Get the URL for voting for choice1
        vote_url = reverse('polls:vote', args=[self.question.id])
        # Submit a POST request to vote for choice1
        response = self.client.post(vote_url, {'choice': self.choice1.id})
        # Check if the response redirects to the results page for the question
        self.assertRedirects(response,
                             reverse('polls:results', args=[self.question.id]))

    def test_user_can_change_vote(self):
        """Test that a user can change their vote by deleting the old one."""
        self.client.login(username='testuser', password='password')
        # Cast vote for choice1
        vote_url = reverse('polls:vote', args=[self.question.id])
        response1 = self.client.post(vote_url, {'choice': self.choice1.id})
        # Check that the user voted for choice1
        self.assertEqual(response1.status_code, 302)
        # Get the user's vote for choice1
        vote = Vote.objects.filter(
            choice__question=self.choice1.question,
            user=self.user
            )
        # Replace 'new_choice' with the choice that user change to
        new_choice = self.choice2
        vote.delete()  # Delete the old vote
        new_vote = Vote.objects.create(choice=new_choice, user=self.user)
        # Ensure that the user's old vote for choice1 is deleted
        self.assertEqual(
            Vote.objects.filter(choice=self.choice1, user=self.user).count(),
            0
        )
        # Ensure that the user's new vote for 'new_choice' is recorded
        self.assertEqual(
            Vote.objects.filter(choice=new_choice, user=self.user).count(),
            1
        )
