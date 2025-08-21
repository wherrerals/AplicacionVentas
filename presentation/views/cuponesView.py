# cupones/views.py
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import transaction
from django.contrib import messages

from infrastructure.models.couponsdb import CouponsDB
from presentation.forms.cuponesForm import CuponForm, CouponRuleRelationFormSet, CouponCollectionsFormSet


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
    """CreateView - Sin cambios, funciona perfectamente"""
    model = CouponsDB
    form_class = CuponForm
    template_name = 'cupones/form.html'
    success_url = reverse_lazy('listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['rules_formset'] = CouponRuleRelationFormSet(self.request.POST)
            context['collections_formset'] = CouponCollectionsFormSet(self.request.POST)
        else:
            context['rules_formset'] = CouponRuleRelationFormSet()
            context['collections_formset'] = CouponCollectionsFormSet()
        context['form_title'] = 'Crear Cupón'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        rules_formset = context['rules_formset']
        collections_formset = context['collections_formset']
        if form.is_valid() and rules_formset.is_valid() and collections_formset.is_valid():
            self.object = form.save()
            rules_formset.instance = self.object
            rules_formset.save()
            collections_formset.instance = self.object
            collections_formset.save()
            messages.success(self.request, 'Cupón creado exitosamente.')
            return redirect(self.success_url)
        return self.form_invalid(form)


class CuponUpdateView(UpdateView):
    """UpdateView - CORREGIDO para manejar formsets correctamente"""
    model = CouponsDB
    form_class = CuponForm
    template_name = 'cupones/form.html'
    success_url = reverse_lazy('listar')
    slug_field = 'cupon_code'
    slug_url_kwarg = 'codigo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.POST:
            # CRÍTICO: Usar prefixes para evitar conflictos
            context['rules_formset'] = CouponRuleRelationFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object,
                prefix='rules'
            )
            context['collections_formset'] = CouponCollectionsFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object,
                prefix='collections'
            )
        else:
            # GET request - cargar datos existentes
            context['rules_formset'] = CouponRuleRelationFormSet(
                instance=self.object,
                prefix='rules'
            )
            context['collections_formset'] = CouponCollectionsFormSet(
                instance=self.object,
                prefix='collections'
            )
        
        context['form_title'] = 'Editar Cupón'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        rules_formset = context['rules_formset']
        collections_formset = context['collections_formset']

        # Debug para desarrollo (remover en producción)
        print("=== UPDATE DEBUG ===")
        print(f"Form valid: {form.is_valid()}")
        print(f"Rules formset valid: {rules_formset.is_valid()}")
        print(f"Collections formset valid: {collections_formset.is_valid()}")
        
        if not rules_formset.is_valid():
            print("Rules formset errors:", rules_formset.errors)
            print("Rules non-form errors:", rules_formset.non_form_errors())
        
        if not collections_formset.is_valid():
            print("Collections formset errors:", collections_formset.errors)
            print("Collections non-form errors:", collections_formset.non_form_errors())

        # Validar todos los forms
        if not (form.is_valid() and rules_formset.is_valid() and collections_formset.is_valid()):
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                # Guardar el objeto principal
                self.object = form.save()

                # CRÍTICO: Configurar instancia antes de guardar
                rules_formset.instance = self.object
                collections_formset.instance = self.object
                
                # Guardar formsets
                rules_formset.save()
                collections_formset.save()

                messages.success(self.request, 'Cupón actualizado exitosamente.')
                return redirect(self.success_url)
                
        except Exception as e:
            print(f"Error saving: {str(e)}")
            messages.error(self.request, f'Error al actualizar el cupón: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Manejo de errores mejorado"""
        context = self.get_context_data()
        rules_formset = context['rules_formset']
        collections_formset = context['collections_formset']
        
        # Debug detallado para desarrollo
        print("=== FORM ERRORS DEBUG ===")
        print("Form errors:", form.errors)
        print("Rules formset errors:", rules_formset.errors)
        print("Collections formset errors:", collections_formset.errors)
        
        messages.error(self.request, 'Por favor corrige los errores del formulario.')
        return super().form_invalid(form)


class CuponDeleteView(DeleteView):
    model = CouponsDB
    template_name = 'cupones/eliminar.html'
    context_object_name = 'cupon'
    slug_field = 'cupon_code'
    slug_url_kwarg = 'codigo'
    success_url = reverse_lazy('listar')


class CuponDetailView(DetailView):
    model = CouponsDB
    template_name = 'cupones/detail.html'
    context_object_name = 'cupon'
    slug_field = 'cupon_code'
    slug_url_kwarg = 'codigo'