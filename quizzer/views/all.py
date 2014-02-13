from django.views.generic import ListView

__author__ = 'tunde'

class AllQuestionsView(ListView):
    paginate_by = 50