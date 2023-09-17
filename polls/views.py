from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages

from .models import Choice, Question, Vote
from django.utils import timezone


class IndexView(generic.ListView):
    """
    View for displaying the list of the latest published questions.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """
    View for displaying the details of a specific question.
    """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_previous_choice(self):
        """
        Get the previous choice made by the user for the current question.
        """
        user = self.request.user
        if user == AnonymousUser():
            return None

        question = self.get_object()
        votes = Vote.objects.filter(choice__question=question,user=user)
        if votes.exists():
            return votes.first().choice
        else:
            return None

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the template.
        """
        context = super().get_context_data(**kwargs)
        context['previous_choice'] = self.get_previous_choice()
        return context


class ResultsView(generic.DetailView):
    """
    View for displaying the results of a specific question.
    """
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    """
    View for handling user votes on a question.
    Returns A redirect to the results page or
    a rendering of the detail page with an error message.
    """
    user = request.user
    print("current user is", user.id, "login", user.username)
    print("Real name:", user.first_name, user.last_name)
    
    if not user.is_authenticated:
       return redirect('login')
    
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "This poll cannot be voted on at this time!!!"
        })
    
    try:
        selected_choice = question.choice_set.get(
        pk=request.POST['choice']
        )
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
            })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        votes = Vote.objects.filter(choice__question=selected_choice.question, user=user)
        
        if votes.exists():
            vote = Vote.objects.get(choice__question=selected_choice.question, user=user)
            vote.choice = selected_choice
        else:
            vote = Vote(choice=selected_choice, user=user)
        vote.save()

        # Add a success message
        messages.success(request, " Your vote has been recorded! ")
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id,))
        )