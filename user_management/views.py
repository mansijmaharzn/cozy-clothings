from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin

from user_management.forms import RegistrationForm


class RegisterView(View):
    template_name = 'user_management/register.html'

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users/login/')

        return render(request, self.template_name, {'form': form})
    

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("/login/")