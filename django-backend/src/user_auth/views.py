from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm

from category.models import Category
from user_auth.forms import AuthForm


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    authentication_form = AuthenticationForm
    template_name = 'user_auth/registration.html'


class MyLogoutView(LogoutView):
    template_name = 'category/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Category.objects.all()
        return context

