from django.contrib import admin
from .models import Category

class CategoriesAdmin(admin.ModelAdmin):
    search_fields = ('title',)  # Ensure 'title' is a field in your Category model

# Register your models here.
admin.site.register(Category, CategoriesAdmin)
