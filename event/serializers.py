from rest_framework import serializers, viewsets
from .models import Loan
from account.serializers import UserDetailsSerializer  # Assuming you have a UserSerializer


class LoanSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)
    payment_schedule = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True) # Для отображения текстового значения статуса

    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['status'] # Чтобы статус нельзя было напрямую изменять через API (опционально)

    def get_payment_schedule(self, obj):
        return obj.generate_payment_schedule()