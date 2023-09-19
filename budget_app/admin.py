from django.contrib import admin

from .models import Category

@admin.register(Category)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'parent_category']