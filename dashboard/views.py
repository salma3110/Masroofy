from django.shortcuts import render
from expenses.models import Log, Category

def dashboard(request):
    # Get all logs from database
    logs = Log.objects.all()
    
    # Calculate total spent
    total_spent = sum(log.amount for log in logs)
    
    # Context to send to template
    context = {
        'total_spent': total_spent,
        'logs': logs,
        'daily_limit': 0,
        'remaining': 0,
    }
    
    return render(request, 'dashboard/dashboard.html', context)