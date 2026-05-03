from django.shortcuts import render, redirect, get_object_or_404
from .models import Log, Category

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
    logs = Log.objects.all().order_by('-date')  # ✅ newest first
    return render(request, 'expenses/history.html', {'logs': logs})


def delete_expense(request, id):
    log = get_object_or_404(Log, id=id)  # ✅ safer lookup
    log.delete()
    return redirect('history')
