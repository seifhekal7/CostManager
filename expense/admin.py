from django.contrib import admin
from .models import Category, Expense, Budget


class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 0
    fields = ('title', 'amount', 'date')
    readonly_fields = ('date',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'description')
    list_filter = ('user',)
    search_fields = ('name', 'description', 'user__email')
    list_per_page = 25
    inlines = [ExpenseInline]   # خلي الـ inline هنا فقط


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'amount', 'user', 'category', 'date', 'created_at')
    list_filter = ('user', 'category', 'date')
    search_fields = ('title', 'category__name', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'date')
    date_hierarchy = 'date'
    ordering = ('-date',)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'month', 'year', 'amount', 'created_at')
    list_filter = ('user', 'category', 'month', 'year')
    search_fields = ('user__email', 'category__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-year', '-month')
