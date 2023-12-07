from django.views.generic import TemplateView
from products.models import Items
# Create your views here.
from django.db.models import Sum


class IndexPageView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context['query_results'] = Items.objects.all()
        return context

class BackPageView(TemplateView):
    template_name = 'main/back.html'

    def get_context_data(self, **kwargs):
        context = super(BackPageView, self).get_context_data(**kwargs)
        context['sum'] = Items.objects.aggregate(Sum('price'))
        return context
