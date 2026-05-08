

"""
@file expenses/models.py
@brief Models for expense tracking: Category and Log.

Defines a simple category model and a `Log` model representing individual
expense entries.
"""

from django.db import models


class Category(models.Model):
    """
    @brief Expense category (e.g., Food, Transport).

    @var name Human readable category name
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Log(models.Model):
    """
    @brief Expense log entry.

    Stores amount, creation date and a foreign key to `Category`.
    @var amount Expense amount as float
    @var date Date of the log (auto set on create)
    @var category ForeignKey to Category
    """
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.amount)
