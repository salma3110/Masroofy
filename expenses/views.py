"""
@file expenses/views.py
@brief Views to add, list, delete and export expense logs.

Simple CRUD-like views for expense entries used by the app UI.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Log, Category
import csv


def add_expense(request):
    """
    @brief Add a new expense log from a submitted form.

    Validates the amount and creates a `Log` instance referencing a
    `Category`.

    @param request Django HTTP request
    @return Django HTTP response or redirect
    """
    if request.method == "POST":
        amount = float(request.POST['amount'])

        if amount < 0:
            return render(request, 'expenses/add_expense.html', {
                'error': 'Amount cannot be negative'
            })

        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)

        Log.objects.create(amount=amount, category=category)
        return redirect('history')

    categories = Category.objects.all()
    return render(request, 'expenses/add_expense.html', {'categories': categories})


def history(request):
    """
    @brief Render a chronological list of expense logs.

    @param request Django HTTP request
    @return Django HTTP response
    """
    logs = Log.objects.all().order_by('-date')
    return render(request, 'expenses/history.html', {'logs': logs})


def delete_expense(request, id):
    """
    @brief Delete a specified expense log by id.

    @param request Django HTTP request
    @param id Primary key of the Log to delete
    @return Django HTTP redirect to history
    """
    log = get_object_or_404(Log, id=id)
    log.delete()
    return redirect('history')


def export_expenses_csv(request):
    """
    @brief Export all expenses as a CSV download.

    @param request Django HTTP request
    @return HttpResponse streaming CSV data
    """
    logs = Log.objects.all().order_by('-date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Category', 'Date'])

    for log in logs:
        writer.writerow([log.amount, log.category.name, str(log.date)])

    return response
