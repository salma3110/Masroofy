from django.db import models
from django.utils import timezone
from expenses.models import Log



class BudgetCycle(models.Model):
    allowance = models.FloatField(default=0.0)
    start_date = models.DateField()
    end_date = models.DateField()
    safe_limit = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"BudgetCycle ({self.start_date} → {self.end_date}) | Allowance: {self.allowance}"

    def set_allowance(self, amount: float) -> None:
        """Validates and stores the allowance. Raises ValueError for non-positive values."""
        if amount <= 0:
            raise ValueError("Allowance must be positive")
        self.allowance = amount
        self.calculate_limit()
        self.save()

    def get_allowance(self) -> float:
        return self.allowance

    def calculate_limit(self) -> float:
        """Calculates safe daily limit based on remaining allowance and days left."""
        today = timezone.now().date()
        remaining_days = (self.end_date - today).days + 1

        if remaining_days <= 0:
            self.safe_limit = 0.0
            return 0.0

        total_spent = self._get_total_spent()
        remaining_balance = self.allowance - total_spent

        if remaining_days == 1:
            self.safe_limit = max(0.0, remaining_balance)
        else:
            self.safe_limit = max(0.0, remaining_balance / remaining_days)

        return self.safe_limit

    def update_limit(self) -> None:
        """Recalculates and persists the limit (handles daily rollover)."""
        self.calculate_limit()
        self.save()

    def calc_threshold(self) -> dict:
        """Returns spending percentage and alert flags (80% and 100%)."""
        if self.allowance <= 0:
            return {"percentage": 0.0, "warn_80": False, "exhausted": False}

        total_spent = self._get_total_spent()
        percentage = (total_spent / self.allowance) * 100

        return {
            "percentage": round(percentage, 2),
            "warn_80": percentage >= 80,
            "exhausted": percentage >= 100,
        }

    def push_alert(self) -> str | None:
        """Returns an alert message string if a threshold is crossed, else None."""
        threshold = self.calc_threshold()
        if threshold["exhausted"]:
            return "Budget exhausted"
        if threshold["warn_80"]:
            return "Warning: 80% of budget used"
        return None

    def _get_total_spent(self) -> float:

        logs_in_cycle = Log.objects.filter(
            date__gte=self.start_date, 
            date__lte=self.end_date
        )
        return logs_in_cycle.aggregate(total=models.Sum('amount'))['total'] or 0.0