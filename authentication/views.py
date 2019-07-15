from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import CustomRegistrationForm

# Create your views here.
class RegistrationView(FormView):
    disallowed_url = 'registration_disallowed'
    form_class = CustomRegistrationForm
    success_url = None
    template_name = 'registration/registration_form.html'

    def dispatch(self, *args, **kwargs):
        if not self.registration_allowed():
            return redirect(self.disallowed_url)
        return super(RegistrationView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        new_user = self.register(form)
        success_url = self.get_success_url(new_user)

        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def registration_allowed(self):
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def register(self, form):
        raise NotImplementedError

