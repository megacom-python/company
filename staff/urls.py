from django.urls import path
from staff import views

urlpatterns = [
    path("departments/", views.MostExpensiveDepartmentAPIView.as_view()),
    path("age-difference/", views.AgeDifferenceView.as_view())
]