import django_tables2 as tables
from quizzer.models import AnswerLogs

class ReportTable(tables.Table):
    class Meta:
        model = AnswerLogs
        attrs = {'class': ''}
        exclude = ('user', 'question', 'id')
        sequence = ('answer', 'time')
        order_by = ('-time',)
        template = 'tables/table.html'
        empty_text = 'Nothing yet!'
