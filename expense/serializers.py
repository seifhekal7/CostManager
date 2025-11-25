from rest_framework import serializers
from .models import Category, Expense, Budget
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # GET only
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    def validate(self, data):
        user = self.context['request'].user
        category = data.get('category') or getattr(self.instance, 'category', None)
        amount = data.get('amount') or getattr(self.instance, 'amount', None)

        if self.instance:
            date = self.instance.date
        else:
            date = timezone.now().date()

        return data

    class Meta:
        model = Expense
        fields = [
            'id', 'amount', 'date', 'title',
            'category',
            'category_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['date', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            # هنا بنخلي الـ category_id يقبل بس الـ categories بتاعة اليوزر الحالي
            self.fields['category_id'].queryset = Category.objects.filter(user=request.user)

    



class BudgetSerializer(serializers.ModelSerializer):
    spent = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)  # GET only
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Budget
        fields = [
            'id',
            'category',     
            'category_id',  
            'month',
            'year',
            'amount',
            'spent',
            'remaining',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'created_at', 'updated_at', 'spent', 'remaining'
        ]

    def get_spent(self, obj):
        total = Expense.objects.filter(
            user=obj.user,
            category=obj.category,
            date__year=obj.year,
            date__month=obj.month
        ).aggregate(total=Sum('amount'))['total']
        return total or Decimal('0.00')

    def get_remaining(self, obj):
        return obj.amount - self.get_spent(obj)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            self.fields['category_id'].queryset = Category.objects.filter(user=request.user)
