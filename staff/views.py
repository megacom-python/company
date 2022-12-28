from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import MostExpensiveDepartmentSerializer, AgeDifferenceSerializer
from .models import Department, Employee, Salary
from django.db.models import Subquery, Count, Sum, Q, OuterRef, Avg
from django.db.models import DurationField, IntegerField, F, Func

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


class AgeYears(Func):
    template = 'EXTRACT (YEAR FROM %(function)s(%(expressions)s))'
    function = 'AGE'
    output_field = IntegerField()


class AgeDifferenceView(ListAPIView):
    # queryset = Employee.objects.filter(subordinates__isnull=False).distinct()
    serializer_class = AgeDifferenceSerializer

    def get_queryset(self):
        queryset = (
            Employee.objects
            # .prefetch_related("subordinates")
            .filter(subordinates__isnull=False)
            .annotate(
                diff=AgeYears(F("date_of_birth")) - Avg(AgeYears(F("subordinates__date_of_birth")))
            )
        )
        """
        SELECT m.email
         , EXTRACT(YEAR FROM AGE(m.date_of_birth))              AS age
         , EXTRACT(YEAR FROM AGE(m.date_of_birth)) - AVG(s.age) AS diff
        FROM staff_employee AS m
                 JOIN (SELECT manager_id, EXTRACT(YEAR FROM AGE(staff_employee.date_of_birth)) AS age
                       FROM staff_employee
                       WHERE manager_id IS NOT NULL) AS s
                      ON m.id = s.manager_id
        GROUP BY m.email, m.date_of_birth
        """
        print(queryset.query)
        return queryset