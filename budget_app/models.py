from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    INCOME = 'I'
    EXPENSE = 'E'
    CATEGORY_TYPES = [
        (INCOME, 'Доходы'),
        (EXPENSE, 'Расходы'),
    ]
    category_type = models.CharField(max_length=1, choices=CATEGORY_TYPES)
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        unique_together = ['category_type', 'name']
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    INCOME = 'I'
    EXPENSE = 'E'
    TRANSACTION_TYPES = [
        (INCOME, 'Доходы'),
        (EXPENSE, 'Расходы'),
    ]
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    created = models.DateTimeField(auto_now_add=True)

