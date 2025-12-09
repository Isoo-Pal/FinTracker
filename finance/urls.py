from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name="home"),
    path('', views.RegisterView.as_view(), name="register"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('transaction/add/', views.TransactionView.as_view(), name="transaction_add"),
    path('transaction/list', views.TransactionListView.as_view(), name = "transaction_list"),
    path('goal/add', views.AddGoalView.as_view(), name = "goal_add"),
]
