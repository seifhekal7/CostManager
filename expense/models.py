from django.db import models
from django.conf import settings 
from django.db.models import Sum
from decimal import Decimal

# Create your models here.


class Category(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='categories')

    name=models.CharField(max_length=255)

    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.name

    

class Expense(models.Model):

    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='expenses')
    
    amount=models.DecimalField(max_digits=8 ,decimal_places=2)

    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)

    title=models.CharField(max_length=255)

    date=models.DateField(auto_now_add=True)

    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.title} - {self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    month = models.PositiveSmallIntegerField()  
    year = models.PositiveSmallIntegerField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)  

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'category', 'month', 'year')  # Budget واحد بس لكل user+category+month+year

    def __str__(self):
        return f"{self.user} - {self.category} - {self.month}/{self.year}"
    
    @property
    def spent_amount(self):

        total = Expense.objects.filter(
            user=self.user,
            category=self.category,
            date__year=self.year,
            date__month=self.month,
        ).aggregate(total=Sum('amount'))['total']
        return total or Decimal('0.00')

    @property
    def remaining_amount(self):
        return self.amount - self.spent_amount
