from django.shortcuts import render
from expenses.models import Log, Category
"""
called when someone visits dashboard
brings all expense logs from the database
Calculates total spent
Packages everything into context
Sends it to the HTML template to display
"""
def dashboard(request):
    # Get all logs from database
    logs = Log.objects.all()
    # Calculate total spent
    total_spent = sum(log.amount for log in logs)
    #calculate spending per cat for pie chart
    categories = Category.objects.all()
    category_names=[]
    category_totals=[]
    for cat in categories:
        cat_logs = logs.filter(category=cat)
        cat_total = sum (log.amount for log in cat_logs)
        if cat_total>0:
            category_names.append(cat.name)
            category_totals.append(cat_total)
    # Context to send to template
    context = {
        'total_spent': total_spent,
        'logs': logs,
        'daily_limit': 0,
        'remaining': 0,
        'category_names': category_names,
        'category_totals' : category_totals,
    }
    
    return render(request, 'dashboard/dashboard.html', context)