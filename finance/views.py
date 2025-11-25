from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def home(request):
    return HttpResponse("<h1>Hello</h1>")


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, 'finance/register.html', {'form' : form})
    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'finance/register.html', {'form' : form})

class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'finance/dashboard.html')