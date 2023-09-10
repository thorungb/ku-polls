from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question
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


class ResultsView(generic.DetailView):
    """
    View for displaying the results of a specific question.
    """
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """
    View for handling user votes on a question.
    Returns A redirect to the results page or
    a rendering of the detail page with an error message.
    """
    question = get_object_or_404(Question, pk=question_id)
    if question.can_vote():
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
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(
                reverse('polls:results', args=(question.id,))
            )
    else:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "This poll cannot be voted on at this time!!!"
        })
