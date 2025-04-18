# Generated by Django 4.2.9 on 2025-04-11 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('every_month_pay_date', models.DateField()),
                ('every_month_pay', models.IntegerField(default=0)),
                ('month_count', models.IntegerField()),
                ('month_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('loan_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Активный'), ('PAID', 'Погашен'), ('OVERDUE', 'Просрочен'), ('PENDING', 'Ожидает одобрения'), ('REJECTED', 'Отклонен')], default='PENDING', max_length=10)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loans', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
