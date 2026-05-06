from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Log, Category
import csv


def add_expense(request):
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
    logs = Log.objects.all().order_by('-date')
    return render(request, 'expenses/history.html', {'logs': logs})


def delete_expense(request, id):
    log = get_object_or_404(Log, id=id)
    log.delete()
    return redirect('history')


def export_expenses_csv(request):
    """Export all expenses to CSV file"""
    logs = Log.objects.all().order_by('-date')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Amount', 'Category', 'Date'])
    
    for log in logs:
        writer.writerow([log.amount, log.category.name, str(log.date)])
    
    return response
