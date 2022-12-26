from django.db import models


class Department(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Employee(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    manager = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, related_name="subordinates")

    def __str__(self):
        return self.full_name


class Payment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Salary(Payment):
    pass


class Bonus(Payment):
    reason = models.CharField(max_length=255)


class Penalty(Payment):
    reason = models.CharField(max_length=255)
