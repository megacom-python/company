from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import MostExpensiveDepartmentSerializer, AgeDifferenceSerializer
from .models import Department, Employee, Salary
from django.db.models import Subquery, Count, Sum, Q, OuterRef


class MostExpensiveDepartmentAPIView(ListAPIView):
    serializer_class = MostExpensiveDepartmentSerializer

    def get_queryset(self):
        queryset = Department.objects.all()
        employees_with_penalties = (
            Employee.objects.filter(penalty__reason="absence")
            .annotate(penalty_count=Count("penalty")).filter(penalty_count__gte=2)
            .values_list("id")
        )
        queryset = (
            queryset
            .filter(
                Q(employee__salary__created_at__year=2022) |
                Q(employee__bonus__created_at__year=2022) |
                Q(employee__penalty__created_at__year=2022)
            )
            .exclude(employee__in=Subquery(employees_with_penalties))
            .annotate(
                amount=Sum("employee__salary__amount", default=0) +
                       Sum("employee__bonus__amount", default=0) -
                       Sum("employee__penalty__amount", default=0)
            )
        )
        """
        SELECT SUM(s.amount) AS amount
        FROM department
        JOIN employee e ON e.department_id = department.id
        JOIN salary s ON s.employee_id = e.id
        WHERE EXTRACT(YEAR FROM s.created_at) = 2022
        """
        print(queryset.query)
        return queryset

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     instance = queryset.order_by("-amount").first()
    #     serializer = self.get_serializer(instance, many=False)
    #     return Response(serializer.data)

class AgeDifferenceView(ListAPIView):
    queryset = Employee.objects.filter(subordinates__isnull=False)
    serializer_class = AgeDifferenceSerializer