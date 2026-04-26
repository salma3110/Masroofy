from django.apps import AppConfig

class ExpensesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expenses'

    def ready(self):
        from .models import Category
        defaults = ["Food", "Transport", "Entertainment", "Bills", "Other"]
        for name in defaults:
            Category.objects.get_or_create(name=name)
