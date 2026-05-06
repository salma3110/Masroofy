from django.shortcuts import render
from expenses.models import Log, Category
from BudgetCycle.models import BudgetCycle
from django.utils import timezone 
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

    # get active budget cycle 
    cycle = BudgetCycle.objects.filter (is_active=True).first()

    # Calculate total spent
    total_spent = sum(log.amount for log in logs)

    # get budget info from cycle if exists 
    daily_limit =0
    remaining = 0
    alert_message= None
    threshold = None

    if cycle:
        cycle.update_limit()
        daily_limit = round(cycle.safe_limit, 2)
        remaining = round(cycle.allowance - cycle._get_total_spent(), 2)
        alert_message = cycle.push_alert()
        threshold = cycle.calc_threshold()


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
        'daily_limit': daily_limit,
        'remaining': remaining,
        'logs': logs,
        'category_names': category_names,
        'category_totals' : category_totals,
        'alert_message': alert_message,
        'threshold': threshold,


    }
    
    return render(request, 'dashboard/dashboard.html', context)