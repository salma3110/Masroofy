from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import date
from .models import BudgetCycle



def _get_active_cycle():
    return BudgetCycle.objects.filter(is_active=True).first()




def setup(request):
    if request.method == 'POST':
        allowance_raw = request.POST.get('allowance', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')

        # Validate allowance
        try:
            allowance = float(allowance_raw)
            if allowance <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            messages.error(request, "Allowance must be a positive number.")
            return render(request, 'BudgetCycle/setup.html')

        # Validate dates
        try:
            sd = date.fromisoformat(start_date)
            ed = date.fromisoformat(end_date)
        except ValueError:
            messages.error(request, "Invalid date format.")
            return render(request, 'BudgetCycle/setup.html')

        if ed <= sd:
            messages.error(request, "End date must be after start date.")
            return render(request, 'BudgetCycle/setup.html')

        # Deactivate old cycle
        BudgetCycle.objects.filter(is_active=True).update(is_active=False)

        # Create new cycle
        cycle = BudgetCycle(
            start_date=sd,
            end_date=ed,
            is_active=True
        )
        cycle.allowance = allowance
        cycle.calculate_limit()
        cycle.save()

        return redirect('budget_cycle:status')

    return render(request, 'BudgetCycle/setup.html')



def change_budget(request):
    cycle = _get_active_cycle()

    if not cycle:
        return redirect('budget_cycle:setup')

    if request.method == 'POST':
        allowance_raw = request.POST.get('allowance', '')
        end_date_raw = request.POST.get('end_date', '')

        # Validate allowance
        try:
            allowance = float(allowance_raw)
            if allowance <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            messages.error(request, "Allowance must be a positive number.")
            return render(request, 'BudgetCycle/change_budget.html', {'cycle': cycle})

        # Update end date if provided
        if end_date_raw:
            try:
                new_end = date.fromisoformat(end_date_raw)
                if new_end <= cycle.start_date:
                    messages.error(request, "End date must be after start date.")
                    return render(request, 'BudgetCycle/change_budget.html', {'cycle': cycle})
                cycle.end_date = new_end
            except ValueError:
                messages.error(request, "Invalid date format.")
                return render(request, 'BudgetCycle/change_budget.html', {'cycle': cycle})

        # Update allowance
        cycle.set_allowance(allowance)

        # Optional alert
        alert = cycle.push_alert()
        if alert:
            messages.warning(request, alert)

        return redirect('budget_cycle:status')

    return render(request, 'BudgetCycle/change_budget.html', {'cycle': cycle})



def budget_status(request):
    cycle = _get_active_cycle()

    if not cycle:
        return redirect('budget_cycle:setup')

    # Update calculations
    cycle.update_limit()
    threshold = cycle.calc_threshold()

    total_spent = cycle._get_total_spent()
    remaining_balance = cycle.allowance - total_spent

    today = timezone.now().date()
    days_remaining = (cycle.end_date - today).days + 1
    is_final_day = (days_remaining == 1)

    context = {
        'cycle': cycle,
        'total_spent': round(total_spent, 2),
        'remaining_balance': round(remaining_balance, 2),
        'safe_limit': round(cycle.safe_limit, 2),
        'days_remaining': days_remaining,
        'is_final_day': is_final_day,
        'threshold': threshold,
        'alert_message': cycle.push_alert(),
    }

    return render(request, 'BudgetCycle/budget_status.html', context)