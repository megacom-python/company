from django.contrib import admin
from .models import (
    Employee, Department, Salary, Penalty, Bonus
)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'department')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'amount', 'created_at')


@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'amount', 'created_at')


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'amount', 'created_at')
