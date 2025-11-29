from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.db.models import Sum

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
        transactions = Transaction.objects.filter(user = request.user)
        goal = Goal.objects.filter(user = request.user)
        # calculating total income and expenses
        total_income = Transaction.objects.filter(user=request.user, transaction_type="Income").aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = Transaction.objects.filter(user=request.user, transaction_type="Expense").aggregate(Sum('amount'))['amount__sum'] or 0
        net_savings = total_income - total_expense
        context = {
            'transactions' : transactions,
            'total_income' : total_income,
            'total_expense' : total_expense,
            'net_savings' : net_savings
        }
        return render(request, 'finance/dashboard.html', context)
    
class TransactionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TransactionForm()
        return render(request, 'finance/transaction_form.html', {'form':form})
    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
        return render(request, 'finance/transaction_form.html', {'form' : transaction})
    

class TransactionListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.all()
        return render(request, 'finance/transaction_list.html', {'transactions' : transactions})
    
class AddGoalView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = GoalForm()
        return render(request, 'finance/goal_form.html', {'form' : form})
    
    def post(self, request, *args, **kwargs):
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('dashboard')
        return render(request, 'finance/transaction_form.html', {'form' : form})