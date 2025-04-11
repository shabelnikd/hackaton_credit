from dateutil.relativedelta import relativedelta
from django.db import models
from account.models import UserModel as User, UserAddress
from afiche import settings
from datetime import date, timedelta

from django.utils import timezone

class Loan(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Активный'),
        ('PAID', 'Погашен'),
        ('OVERDUE', 'Просрочен'),
        ('PENDING', 'Ожидает одобрения'),
        ('REJECTED', 'Отклонен'),
    ]

    start_date = models.DateField(default=timezone.now)
    every_month_pay_date = models.DateField()
    every_month_pay = models.IntegerField(default=0)
    month_count = models.IntegerField()
    month_percentage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def generate_payment_schedule(self):
        schedule = []
        current_date = self.start_date
        payment_day = self.every_month_pay_date.day
        outstanding_balance = self.loan_amount or 0  # Текущий остаток долга

        for i in range(self.month_count):
            try:
                payment_date = date(current_date.year, current_date.month, payment_day)
                if payment_date < current_date and i == 0:
                    payment_date += relativedelta(months=1)
                elif payment_date.day != self.every_month_pay_date.day: # Обработка сдвига даты для последующих месяцев
                    payment_date += relativedelta(months=i, day=payment_day)
                    if payment_date < current_date:
                        payment_date += relativedelta(months=1)
            except ValueError:
                import calendar
                last_day = calendar.monthrange(current_date.year, current_date.month)[1]
                payment_date = date(current_date.year, current_date.month, last_day)
                if payment_date < current_date and i == 0:
                    payment_date += relativedelta(months=1, day=last_day)
                elif payment_date.day != last_day: # Обработка сдвига даты для последующих месяцев
                    payment_date = date(self.start_date.year, self.start_date.month, last_day) + relativedelta(months=i)
                    if payment_date < current_date:
                        payment_date += relativedelta(months=1)


            interest_rate = self.month_percentage / 100 if self.month_percentage else 0
            interest_amount = outstanding_balance * interest_rate
            principal_amount = self.every_month_pay - interest_amount

            # Убедитесь, что основной долг не становится отрицательным из-за округления
            if principal_amount > outstanding_balance:
                principal_amount = outstanding_balance
            outstanding_balance -= principal_amount

            schedule.append({
                'payment_date': payment_date,
                'amount': self.every_month_pay,
                'principal': round(principal_amount, 2),
                'interest': round(interest_amount, 2),
                'remaining_balance': round(outstanding_balance, 2),
            })
            current_date += relativedelta(months=1)

        return schedule

    def __str__(self):
        return f"Кредит №{self.id} пользователя {self.user} - Статус: {self.get_status_display()}"

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

