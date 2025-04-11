from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Loan
from .serializers import LoanSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Loan.objects.all()
        else:
            return Loan.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        if not user.is_staff and serializer.instance.user != user:
            raise permissions.Http404("You do not have permission to update this loan.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if not user.is_staff and instance.user != user:
            raise permissions.Http404("You do not have permission to delete this loan.")
        instance.delete()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        loan = self.get_object()
        if loan.status == 'PENDING':
            loan.status = 'ACTIVE'
            loan.save()
            serializer = self.get_serializer(loan)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Кредит уже имеет статус, отличный от "Ожидает одобрения".'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        loan = self.get_object()
        if loan.status == 'PENDING':
            loan.status = 'REJECTED'
            loan.save()
            serializer = self.get_serializer(loan)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Кредит уже имеет статус, отличный от "Ожидает одобрения".'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        loan = self.get_object()
        loan.status = 'PAID'
        loan.save()
        serializer = self.get_serializer(loan)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_overdue(self, request, pk=None):
        loan = self.get_object()
        loan.status = 'OVERDUE'
        loan.save()
        serializer = self.get_serializer(loan)
        return Response(serializer.data)