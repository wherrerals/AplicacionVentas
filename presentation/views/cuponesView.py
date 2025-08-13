# cupones/views.py
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy

from infrastructure.models.couponsdb import CouponsDB
from presentation.forms.cuponesForm import CuponForm


class CuponListView(ListView):
    model = CouponsDB
    template_name = 'cupones/list.html'
    context_object_name = 'cupones'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(cupon_code__icontains=q)
        return queryset.order_by('-last_modification')

class CuponCreateView(CreateView):
    model = CouponsDB
    form_class = CuponForm
    template_name = 'cupones/form.html'
    success_url = reverse_lazy('listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Crear Cupón'
        return context

class CuponUpdateView(UpdateView):
    model = CouponsDB
    form_class = CuponForm
    template_name = 'cupones/form.html'
    success_url = reverse_lazy('listar')
    slug_field = 'cupon_code'
    slug_url_kwarg = 'codigo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Cupón'
        return context

class CuponDetailView(DetailView):
    model = CouponsDB
    template_name = 'cupones/detail.html'
    context_object_name = 'cupon'
    slug_field = 'cupon_code'
    slug_url_kwarg = 'codigo'
