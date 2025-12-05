from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clients/', views.clients, name='client_dashboard'),

    path('api/loan/', views.loan_eligibility, name='loan_eligibility'),
    path('api/salary/<str:national_id>/', views.salary_verification, name='salary_verification'),
    path('api/credit/<str:national_id>/', views.credit_bureau, name='credit_bureau'),
    path('', views.index, name='index'),
]
