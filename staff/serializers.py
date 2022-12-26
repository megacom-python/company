from rest_framework import serializers
from .models import Department, Employee
from datetime import date
import math


def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

class MostExpensiveDepartmentSerializer(serializers.ModelSerializer):
    amount = serializers.ReadOnlyField()

    class Meta:
        model = Department
        fields = "__all__"


class AgeDifferenceSerializer(serializers.ModelSerializer):
    diff = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = "__all__"

    def get_diff(self, obj: Employee):
        manager_age = age(obj.date_of_birth)
        subordinate_ages = [age(sub.date_of_birth) for sub in obj.subordinates.all()]
        avg_age = sum(subordinate_ages)/len(subordinate_ages)
        return manager_age - avg_age