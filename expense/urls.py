from django .urls import path
from .views import (
    CategoryListCreateView, ExpenseListCreateView, BudgetListCreateView,
    CategoryDetailView, ExpenseDetailView, BudgetDetailView
)
urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),

    path('budgets/', BudgetListCreateView.as_view(), name='budget-list'),
    path('budgets/<int:pk>/', BudgetDetailView.as_view(), name='budget-detail'),
]